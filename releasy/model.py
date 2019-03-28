"""
Releasy Meta Model
"""
from __future__ import annotations
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
        self.authors = []
        self._config_ctrl = []
        self.release_pattern = None

        self.load_config()

        if regexp:
            self.release_pattern = re.compile(regexp)
            self._config_ctrl.append('release_pattern')
        if not self.release_pattern: # default
            self.release_pattern = re.compile(r'(?P<major>[0-9]{1,3})([\._](?P<minor>[0-9]+))([\._](?P<patch>[0-9]+))?')

    @property
    def vcs(self) -> Vcs:
        return self.__vcs

    @vcs.setter
    def vcs(self, vcs: Vcs):
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
        merges: list of merge commits that belong exclusively to this release
        tag: tag that represents the release
        head: commit referred  by release.tag
        tails: list of commits where the release begin
        developers: list of authors and committers
        committers: list of committers
        authors: list of authors
    """

    def __init__(self, project, tag):
        self.project = project
        self.tag = tag
        self.commits = []
        self.merges = []
        self.tails = []
        self.developers = DeveloperRoleTracker()

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
    def commit_count(self):
        return len(self.commits)

    @property
    def merge_count(self):
        return len(self.merges)

    @property
    def developer_count(self):
        return len(self.developers)

    @property
    def newcommer_count(self):
        return len(self.newcommers)

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

    @property
    def parents(self):
        return []


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


class ZTracker:
    """ Tracker is a dynamic object to track and agregate contributions """
    
    def __init__(self, items=None):
        self._tracker = {}
        if items:
            for (item, count) in items:
                self.add(item, count)

    def add(self, item, count=1):
        if item in self._tracker:
            self._tracker[item]['count'] += count
        else:
            self._tracker[item] = {
                'count': count
            }
   
    def list(self):
        """ Return the list of tracked objects """
        return self._tracker.keys()

    def items(self):
        """ Return the list of tracked objetcs and the tracked values """
        return self._tracker.items()

    def count(self) -> int:
        """ Return the count of tracked objects """
        return len(self.list())

    def top(self, percent=0.8):
        """ Return the top tracked items

        Params:
            percent: percentage that the top matches, i.g., 0.8 return the
                     tracked items responsible for 80% of the total
        """
        items = sorted(self.items(), key=lambda x:x[1]['count'], reverse=True)
        threshold = min(percent * self.total, self.total)
        amount = 0
        items_iterator = iter(items)
        top = Tracker()
        while amount < threshold:
            item = next(items_iterator)
            amount += item[1]['count']
            top.add(item[0], item[1]['count'])
        return top

# class Tracker:
#     """ Generic tracker """
#     def __init__(self, trackers=None):
#         if trackers:
#             for tracker in trackers:
#                 self.merge(tracker)
    
#     def merge(self, tracker):
#         """ Merge current tracker with other """
#         pass

#     def list(self):
#        """ Return the list of tracked objects """
#        return self._tracker.keys()

  
class DeveloperTracker:
    """ Track developers """
    def __init__(self):
        self._developers = {}
        self._totals = {
            'commits': 0
        }

    def add(self, developer: Developer, commit:Commit):
        if developer and commit:
            if developer in self._developers: 
                self._developers[developer]['commits'].append(commit)
            else:
                self._developers[developer] = { 'commits': [commit] }
            self._totals['commits'] += 1

    def list(self):
        return self._developers.keys()

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
    def __init__(self, trackers: DeveloperTracker=None):
        self.authors = DeveloperTracker()
        self.committers = DeveloperTracker()
        self.newcomers = DeveloperTracker()


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
    release.commits.append(commit)
    if len(commit.parents) > 1:
        release.merges.append(commit)

    release.developers.committers.add(commit.committer, commit)
    release.developers.authors.add(commit.author, commit)

    # if commit.committer not in release.developers:
    #     release.developers.append(commit.committer)
    # if commit.committer not in release.committers:
    #     release.committers.append(commit.committer)

    # release.authors.add(commit.author)
    # if commit.author not in release.developers:
    #      release.developers.append(commit.author)
    # if commit.author not in release.authors:
    #     release.authors.append(commit.author)
    # if commit.author not in project.authors:
    #     project.authors.append(commit.author)
    #     release.newcommers.append(commit.author)


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

