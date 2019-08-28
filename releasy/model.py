"""
Releasy Meta Model
"""
import typing
from datetime import timedelta
import re
import yaml
import os

from .phase import Development, Stage, Maintenance


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
    def __init__(self, name):
        self.name = name
        self._releases = None
        self.commits = CommitTracker()
        self.developers = DeveloperRoleTracker()

    @property
    def releases(self):
        return self._releases

    def __init2__(self, name, path, regexp=None):
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
            self.release_pattern = re.compile(r'^(?:.*?[^0-9\.])?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$')
            # self.release_pattern = re.compile(r'^.*(?P<major>[0-9]+)[\._\-](?P<minor>[0-9]+)[\._\-](?P<patch>[0-9]+)$')

    def __repr__(self):
        return self.name

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


class ReleaseDevelopment():
    def __init__(self):
        self.commits = []
        self.commit = {}
        self.start = None
        self.end = None


class ReleasePre():

    def __init__(self):
        self.releases = []
        self.release = {}

    def add(self, release):
        if release.name not in self.release:
            self.releases.append(release)
            self.release[release.name] = release


class ReleaseMaintenance():

    def __init__(self):
        self.patches = []
        self.patch = {}
        self.start = None
        self.end = None

    def add(self, release):
        if release.name not in self.patch:
            self.patches.append(release)
            self.patch[release.name] = release


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

    def __init__(self, tag, release_type=None, prefix=None, major=None, minor=None, patch=None):
        self._tag = tag
        self.type = release_type
        self.prefix = prefix
        self.major = major
        self.minor = minor
        self.patch = patch
        self.version = "%d.%d.%d" % (self.major, self.minor, self.patch)
        self.base_releases = []
        self.tail_commits = []
        self.commits = CommitTracker()
        self.developers = DeveloperRoleTracker() #TODO remove project
        
    @property
    def name(self):
        return self._tag.name
        
    @property
    def head_commit(self):
        return self._tag.commit

    @property
    def time(self):
        return self._tag.time

    @property
    def length(self):
        return self.time - self.tail_commits[0].author_time

    @property
    def description(self):
        return self._tag.message

    def __repr__(self):
        return self.name

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
    def length_group(self):
        if self.length < timedelta(hours=1):
            return 0 #'minutes'
        elif self.length < timedelta(days=1):
            return 1 #'hours'
        elif self.length < timedelta(days=7):
            return 2 #'days'
        elif self.length < timedelta(days=30):
            return 3 #'weeks'
        elif self.length < timedelta(days=365):
            return 4 #'months'
        else:
            return 5 #'years'

    @property
    def length_groupname(self):
        return {
            0: 'minutes',
            1: 'hours',
            2: 'days',
            3: 'weeks',
            4: 'months',
            5: 'years'
        }[self.length_group]
    
    @property
    def churn(self):
        if self.__commit_stats:
            return self.__commit_stats.churn

        self.__commit_stats = CommitStats()
        if self.base_releases:
            for base_release in self.base_releases:
                self.__commit_stats += self.head.diff_stats(base_release.head)
        else:
            self.__commit_stats = self.head.diff_stats()

        return self.__commit_stats.churn


class Tag:
    """Tag

    Attributes:
        name: tag name
        commit: tagged commit
        time: tag time
        message (str): tag message - annotated tags only
    """

    def __init__(self, name, commit, time=None, message=None):
        self.name = name
        self.commit = commit
        if time: # annotated tag
            self.time = time
            self.message = message
        else:
            self.time = commit.committer_time
            self.message = commit.committer_time


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
    def __init__(self, hashcode, parents, message, author, author_time, committer,
                 committer_time):
        self.hashcode = hashcode
        self.parents = parents
        self.message = message
        self.author = author
        self.author_time = author_time
        self.committer = committer
        self.committer_time = committer_time
        self.release = None

    def __repr__(self):
        return str(self.hashcode)

    @property
    def churn(self):
        return self.stats.churn

    @property
    def stats(self):
        return self._stats

    def diff_stats(self, commit):
        pass


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

    def __add__(self, other):
        if other:
            sum = CommitStats()
            sum.insertions = self.insertions + other.insertions
            sum.deletions = self.deletions + other.deletions
            sum.files_changed = self.files_changed + other.files_changed
            return sum
        else:
            return self

    @property
    def churn(self):
        """ return code churn, i.e, insertions + deletions """
        return self.insertions + self.deletions


class CommitTracker():
    def __init__(self):
        self._commits = {}
        self._totals = {
            'churn': -1,
            'merges': 0
        }

    def __len__(self):
        return self.count()

    def add(self, commit):
        if commit:
            if commit not in self._commits: 
                self._commits[commit] = commit 
                if len(commit.parents) > 1:
                    self._totals['merges'] += 1

    def list(self):
        return self._commits.keys()

    def contains(self, commit):
        return commit in self._commits

    def count(self):
        return len(self.list())

    def total(self, metric=None):
        if not metric:
            return self.count()
        elif metric in self._totals:
            # since churn is cpu intensive, we lazy calc them
            if metric == 'churn' and self._totals[metric] == -1: 
                self._totals['churn'] = 0
                for commit in self.list():
                    self._totals['churn'] += commit.churn
            return self._totals[metric]
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
    def __init__(self):
        self._developers = {}
        self._totals = {
            'commits': 0
        }

    def add(self, developer: Developer, commits):
        if developer and commits:
            if not type(commits) is list:
                commits = [commits]
            if developer in self._developers: 
                self._developers[developer]['commits'].extend(commits)
            else:
                self._developers[developer] = { 'commits': commits }
            self._totals['commits'] += len(commits)

    def list(self):
        return self._developers.keys()

    def contains(self, developer):
        return developer in self._developers

    def count(self):
        return len(self.list())

    def total(self, attribute=None):
        if not attribute:
            return self.count()
        elif attribute in self._totals:
            return self._totals[attribute]
        else:
            return -1

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
        top = DeveloperTracker()
        while amount < threshold:
            developer, data = next(developers_it)
            amount += len(data['commits'])
            top.add(developer, data['commits'])
        return top


class DeveloperRoleTracker(DeveloperTracker):
    """ Track developer roles """
    def __init__(self, project=None):
        super().__init__()
        self.project = project
        self.authors = DeveloperTracker()
        self.committers = DeveloperTracker()
        self.newcomers = DeveloperTracker()

