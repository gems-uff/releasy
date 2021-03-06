"""
Releasy Meta Model
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from .release import Release

from .const import RELEASE_TYPE_ANY
from datetime import timedelta
import re
import yaml
import os

#import releasy
from .phase import Development, Stage, Maintenance
from .developer import DeveloperRoleTracker
from .exception import CommitReleaseAlreadyAssigned


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
        self._releases: List[Release] = []
        self.commits = [] #CommitTracker()
        self.developers = DeveloperRoleTracker()
        self.tags: List[Tag] = []

    def _assign_releases(self, releases):
        release_prefixes = {}
        release_suffixes = {}
        for release in releases:
            if release.prefix not in release_prefixes:
                release_prefixes[release.prefix] = 0
            if release.suffix not in release_suffixes:
                release_suffixes[release.suffix] = 0
            release_prefixes[release.prefix] += 1
            release_suffixes[release.suffix] += 1

        self._releases = releases
        self.release_prefixes = release_prefixes
        self.release_suffixes = release_suffixes            

    @property
    def releases(self) -> List[Release]:
        return self.get_releases()

    def get_releases(self, release_type=RELEASE_TYPE_ANY):
        releases = []
        for release in self._releases:
            if release.is_type(release_type):
                releases.append(release)
        return releases

    def __repr__(self):
        return self.name

    @property
    def tagnames(self):
        return self.vcs.tagnames

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

    def add_commit(self, commit: Commit):
        self.commits.append(commit)


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


# class DeveloperDB:
#     """
#     Store developer information and handle developers with multiple ids
#     """

#     def __init__(self):
#         self._developer_db = {}

#     def load_developer(self, login=None, name=None, email=None):
#         if not login:
#             login = email
#         if login not in self._developer_db:
#             developer = Developer()
#             developer.login = login
#             developer.name = name
#             developer.email = email
#             self._developer_db[login] = developer
#         return self._developer_db[login]


# class Developer:
#     """
#     Contributors: Developers and committers

#     Attributes:
#         login: contributor id
#         name: contributor name
#         email: contributor e-mail
#     """

#     def __init__(self):
#         self.login = None
#         self.name = None
#         self.email = None

#     def __repr__(self):
#         return self.login
 

# class DeveloperTracker:
#     """ Track developers """
#     def __init__(self):
#         self._developers = {}
#         self._totals = {
#             'commits': 0
#         }

#     def add(self, developer: Developer, commits):
#         if developer and commits:
#             if not type(commits) is list:
#                 commits = [commits]
#             if developer in self._developers: 
#                 self._developers[developer]['commits'].extend(commits)
#             else:
#                 self._developers[developer] = { 'commits': commits }
#             self._totals['commits'] += len(commits)

#     def list(self):
#         return self._developers.keys()

#     def contains(self, developer):
#         return developer in self._developers

#     def count(self):
#         return len(self.list())

#     def total(self, attribute=None):
#         if not attribute:
#             return self.count()
#         elif attribute in self._totals:
#             return self._totals[attribute]
#         else:
#             return -1

#     def top(self, percent, attribute='commits'):
#         """ Return the top tracked items

#         Params:
#             percent: percentage that the top matches, i.g., 0.8 return the
#                      tracked items responsible for 80% of the total
#         """
#         developers = sorted(self._developers.items(),
#                        key=lambda d:len(d[1]['commits']), 
#                        reverse=True)
#         threshold = min(percent * self._totals['commits'],
#                         self._totals['commits'])
#         amount = 0
#         developers_it = iter(developers)
#         top = DeveloperTracker()
#         while amount < threshold:
#             developer, data = next(developers_it)
#             amount += len(data['commits'])
#             top.add(developer, data['commits'])
#         return top


# class DeveloperRoleTracker(DeveloperTracker):
#     """ Track developer roles """
#     def __init__(self, project=None):
#         super().__init__()
#         self.project = project
#         self.authors = DeveloperTracker()
#         self.committers = DeveloperTracker()
#         self.newcomers = DeveloperTracker()

