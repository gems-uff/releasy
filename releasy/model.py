"""
Releasy Meta Model
"""
import typing

import re
import yaml
import os


class Project:
    """
    Software Project

    Attributes:
        releases: list of project releases, sorted by date
        release_pattern: compiled regexp to match if a tag is a release
        vcs: version control system
        developers: track project developers
        tagnames (readonly): list of tag names
        _config_ctrl: control changes that can be saved in .releasy file
    """

    def __init__(self, name, path, regexp=None):
        self.name = name
        self.path = path
        self.config_path = os.path.join(self.path, '.releasy')
        self.releases = []
        self.__vcs = None
        self.__developer_db = None
        self.developers = DeveloperRoleTracker()
        self._config_ctrl = []
        self.commits = CommitTracker()
        self.release_pattern = None

        self.load_config()

        if regexp:
            self.release_pattern = re.compile(regexp)
            self._config_ctrl.append('release_pattern')
        if not self.release_pattern: # default
            self.release_pattern = re.compile(r'(?P<major>[0-9]{1,3})([\._](?P<minor>[0-9]+))([\._](?P<patch>[0-9]+))?')

    @property
    def vcs(self):
        return self.__vcs

    @vcs.setter
    def vcs(self, vcs):
        self.__vcs = vcs
        self.__vcs.path = self.path
        if self.__developer_db:
            self.__vcs.developer_db = self.developer_db

    @property
    def developer_db(self):
        return self.__developer_db

    @developer_db.setter
    def developer_db(self, developer_db):
        self.__developer_db = developer_db
        if self.__vcs:
            self.__vcs.developer_db = developer_db

    @property
    def tagnames(self):
        return self.vcs.tagnames

    def load(self):
        """ load project data """
        self.__load_releases()
        self.__load_commits()

    def __load_releases(self):
        """ Load release data """
        for tagname in self.tagnames:
            if self.is_release_tag(tagname):
                tag = self.vcs.load_tag(tagname)
                self.releases.append(Release(self, tag))
        self.releases = sorted(self.releases, key=lambda release: release.time)

    def __load_commits(self):
        for release in self.releases:
            track_release(self, release)

    def is_release_tag(self, tagname):
        return is_release_tag(self, tagname)

    def release_pattern_search(self, release_name):
        return release_pattern_search(self.release_pattern, release_name)

    def load_config(self):
        """ load configuration file """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as config_file:
                config = yaml.load(config_file)
                if 'release_pattern' in config:
                    self.release_pattern = re.compile(config['release_pattern'])

    def save_config(self):
        """ save configuration file """
        config = {}
        if 'release_pattern' in self._config_ctrl:
            config['release_pattern'] = self.release_pattern.pattern
        if config:
            with open(self.config_path, 'w') as config_file:
                yaml.dump(config, config_file, default_flow_style=False)


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """

    def __init__(self):
        self._commit_cache = {}
        self._tag_cache = {}
        self.developer_db = None

    def load_tag(self):
        """ load tag from version control """
        pass

    def load_commit(self):
        """ load commit from version control """
        pass


class Release:
    """
    Software Release

    Attributes:
        name (str): release name
        description (str): release description
        time: release creation time
        commits: list of commits that belong exclusively to this release
        tag: tag that represents the release
        head: commit referred  by release.tag
        tails: list of commits where the release begin
        developers: list of developers
        length: release duration
    """

    def __init__(self, project, tag):
        self.project = project
        self.tag = tag
        self.commits = CommitTracker([project.commits])
        self.tails = []
        self.developers = DeveloperRoleTracker(project)

    @property
    def name(self):
        return self.tag.name

    @property
    def description(self):
        return self.tag.message

    @property
    def time(self):
        return self.tag.time

    @property
    def head(self):
        return self.tag.commit

    @property
    def typename(self):
        current = self.project.release_pattern.match(self.name)
        if current:
            if current.group('patch') != '0':
                return 'PATCH'
            elif current.group('minor') != '0':
                return 'MINOR'
            else:
                return 'MAJOR'
        else:
            return 'UNKNOWN'

    @property
    def first_commit(self):
        return self.tails[0]

    @property
    def __start_commit(self):
        """
        The start commit of a release is the first commit
        if the release has at least one commit, or the head
        if the release has no commit.
        """
        if self.tails:
            return self.first_commit
        else:
            return self.head

    @property
    def length(self):
        # return self.time - self.__start_commit.time
        return self.time - self.__start_commit.author_time


class Tag:
    """Tag

    Attributes:
        name: tag name
        commit: tagged commit
        time: tag time
        message (str): tag message - annotated tags only
    """

    def __init__(self):
        self.name = None
        self.commit = None
        self.time = None
        self.message = None


class Commit:
    """
    Commit

    Attributes:
        id: commit id
        message: commit message
        subject: first line from commit message
        commiter: contributor responsible for the commit
        author: contributor responsible for the code
        time: commit time
        author_time: author time
        release: associated release
    """

    def __init__(self):
        self.id = None
        self.subject = None
        self.message = None
        self.committer = None
        self.author = None
        self.release = None
        self.time = None
        self.author_time = None
        self._stats = None

    def __repr__(self):
        return self.id

    @property
    def parents(self):
        return []

    @property
    def churn(self):
        return self.stats.insertions + self.stats.deletions

    @property
    def stats(self):
        return self._stats


class CommitStats():
    """ Store diff stats of commits 
    
    Attributes:
        insertions: number of inserted lines 
        deletions: number of deleted lines
        files_changed: number of changed files
    """
    def __init__(self):
        self.insertions = 0
        self.deletions = 0
        self.files_changed = 0


class CommitTracker():
    def __init__(self, triggers=None):
        self._commits = {}
        self._totals = {
            'churn': 0,
            'merges': 0
        }
        self.triggers = []
        if triggers:
            self.triggers.extend(triggers)

    def add(self, commit):
        if commit:
            if commit not in self._commits: 
                self._commits[commit] = 1 
            self._totals['churn'] += commit.churn
            if len(commit.parents) > 1:
                self._totals['merges'] += 1
            for trigger in self.triggers:
                trigger.add(commit)

    def list(self):
        return self._commits.keys()

    def contains(self, commit):
        return commit in self._commits

    def count(self):
        return len(self.list())

    def total(self, attribute):
        if attribute in self._totals:
            return self._totals[attribute]
        else:
            return -1


class DeveloperDB:
    """
    Store developer information and handle developers with multiple ids
    """

    def __init__(self):
        self._developer_db = {}

    def load_developer(self, login=None, name=None, email=None):
        if not login:
            login = email
        if login not in self._developer_db:
            developer = Developer()
            developer.login = login
            developer.name = name
            developer.email = email
            self._developer_db[login] = developer
        return self._developer_db[login]


class Developer:
    """
    Contributors: Developers and committers

    Attributes:
        login: contributor id
        name: contributor name
        email: contributor e-mail
    """

    def __init__(self):
        self.login = None
        self.name = None
        self.email = None

    def __repr__(self):
        return self.login
 

class DeveloperTracker:
    """ Track developers """
    def __init__(self, triggers=None):
        self._developers = {}
        self._totals = {
            'commits': 0
        }
        self.triggers = []
        if triggers:
            self.triggers.extend(triggers)

    def add(self, developer: Developer, commit:Commit):
        if developer and commit:
            if developer in self._developers: 
                self._developers[developer]['commits'].append(commit)
            else:
                self._developers[developer] = { 'commits': [commit] }
            self._totals['commits'] += 1
            for trigger in self.triggers:
                trigger.add(developer, commit)

    def list(self):
        return self._developers.keys()

    def contains(self, developer):
        return developer in self._developers

    def count(self):
        return len(self.list())

    def top(self, percent, attribute='commits'):
        """ Return the top tracked items

        Params:
            percent: percentage that the top matches, i.g., 0.8 return the
                     tracked items responsible for 80% of the total
        """
        developers = sorted(self._developers.items(),
                       key=lambda d:len(d[1]['commits']), 
                       reverse=True)
        threshold = min(percent * self._totals['commits'],
                        self._totals['commits'])
        amount = 0
        developers_it = iter(developers)
        top = []
        while amount < threshold:
            item = next(developers_it)
            amount += len(item[1]['commits'])
            top.append(item[0])
        return top


class DeveloperRoleTracker(DeveloperTracker):
    """ Track developer roles """
    def __init__(self, project=None):
        super().__init__()
        self.project = project
        authors_triggers = [self]
        committers_triggers = [self]
        if project:
            authors_triggers.append(project.developers.authors)
            committers_triggers.append(project.developers.committers)

        self.authors = DeveloperTracker(authors_triggers)
        self.committers = DeveloperTracker(committers_triggers)
        self.newcomers = DeveloperTracker()

    def add(self, developer: Developer, commit:Commit):
        if self.project:
            if not self.project.developers.contains(developer):
                self.newcomers.add(developer, commit)
        super().add(developer, commit)

def is_release_tag(project, tagname):
    """ Check if a tag represents a release """
    if project.release_pattern.search(tagname):
        return True
    return False


def is_tracked_commit(commit):
    """ Check if commit is tracked on a release """
    if commit.release:
        return True
    return False


def track_release(project, release):
    """
    Associate release to it commits

    Params:
        release: release list sorted by date
    """

    commit_stack = [ release.head ]
    while len(commit_stack):
        cur_commit = commit_stack.pop()

        # handle multiple tags pointing to a single commit
        if not is_tracked_commit(cur_commit):
            track_commit(project, release, cur_commit)

            is_tail = False
            if cur_commit.parents:
                for parent_commit in cur_commit.parents:
                    if is_tracked_commit(parent_commit):
                        is_tail = True
                    else:
                        commit_stack.append(parent_commit)
            else:
                is_tail = True
            if is_tail:
                release.tails.append(cur_commit)

    # release.tails = sorted(release.tails, key=lambda commit: commit.time)
    release.tails = sorted(release.tails, key=lambda commit: commit.author_time)


def track_commit(project, release, commit):
    " associate commit to release "
    commit.release = release
    release.commits.add(commit)
    release.developers.committers.add(commit.committer, commit)
    release.developers.authors.add(commit.author, commit)


def release_pattern_search(pattern, release_name):
    re_match = pattern.search(release_name)
    if re_match:
        major = re_match.group('major')
        minor = re_match.group('minor')
        patch = re_match.group('patch')

        if patch and patch != '0':
            type = 'PATCH'
        elif minor and minor != '0':
            type = 'MINOR'
        elif major:
            type = 'MAJOR'
        else:
            type = 'UNKNOWN'
        return type, major, minor, patch

