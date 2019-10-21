from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .model import Commit, Project

import re
from datetime import timedelta

from .model import Tag, CommitTracker
from .developer import ReleaseDeveloperRoleTracker
from .exception import CommitReleaseAlreadyAssigned, MisplacedTimeException


class ReleaseFactory():
    def __init__(self, project: Project, prefixes=None, suffixes=None):
        self._project = project
        self._pre_release_cache = {}
        self.prefixes = prefixes
        self.suffixes = suffixes

    def get_release(self, tag: Tag):
        release_info = self._match_release(tag.name)
        if not release_info:
            return None
        else:
            (release_type, prefix, suffix, major, minor, patch) = release_info
            release_version = f"{major}.{minor}.{patch}"

        if self.prefixes and prefix not in self.prefixes:
            return None

        if release_version not in self._pre_release_cache:
            self._pre_release_cache[release_version] = []

        if release_type == "PRE":
            release = PreRelease(project=self._project, 
                                    tag=tag,
                                    release_type="PRE",
                                    prefix=prefix,
                                    major=major,
                                    minor=minor,
                                    patch=patch)
            self._pre_release_cache[release_version].append(release)
        else:
            release = Release(project=self._project,
                                tag=tag, 
                                release_type="release_type",
                                prefix=prefix, 
                                major=major, 
                                minor=minor, 
                                patch=patch)
            for pre_release in self._pre_release_cache[release_version]:
                release.add_pre_release(pre_release)

        tag.release = release
        return release

    def _match_release(self, tagname):
        pattern = re.compile(r"^(?P<prefix>(?:.*?[^0-9\.]))?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?((?P<suffix>-?(?P<pre>.+)))?$")
        re_match = pattern.search(tagname)
        if re_match:
            prefix = re_match.group("prefix")
            suffix = re_match.group("suffix")
            major_version = 0
            minor_version = 0
            patch_version = 0
            pre_release = re_match.group("pre")

            major = re_match.group("major")
            if major:
                major_version = int(major)

            minor = re_match.group("minor")
            if minor:
                minor_version = int(minor)

            patch = re_match.group("patch")
            if patch:
                patch_version = int(patch)
            else:
                patch_version = 0

            if pre_release:
                release_type = "PRE"
            elif patch_version > 0:
                release_type = "PATCH"
            elif minor_version > 0:
                release_type = "MINOR"
            else: # major_version > 0:
                release_type = "MAJOR"

            return (release_type,
                    prefix,
                    suffix,
                    major_version,
                    minor_version,
                    patch_version)
        else:        
            return False


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

    def __init__(self, project: Project, tag, release_type=None, prefix=None, major=None, minor=None, patch=None):
        self.project = project
        self._tag = tag
        self.type = release_type
        self.prefix = prefix
        self.major = major
        self.minor = minor
        self.patch = patch
        self.version = f"{major}.{minor}.{patch}"
        self.feature_version = f"{major}.{minor}.x"
        self.base_releases = []
        self.reachable_releases = []
        self.tail_commits = []
        self.commits = []
        self.developers = ReleaseDeveloperRoleTracker()
        self.pre_releases = []
        self.patches = []
        self.previous_release: Release = None
        self.next_release: Release = None
        self.previous_feature_release: Release = None
        self.next_feature_release: Release = None
        
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
        if self.tail_commits:
            length = self.time - self.tail_commits[0].author_time
        else:
            length = self.time - self.head_commit.author_time
        
        if length < timedelta(0):
            raise MisplacedTimeException(self)
        return length

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

    def is_patch(self) -> bool:
        return self.patch != 0

    def is_pre_release(self) -> bool:
        return self.type == "PRE"

    def add_commit(self, commit: Commit, assign_commit_to_release=True):
        is_newcomer = False
        if assign_commit_to_release:
            if not commit.release:
                commit.release = self
                self.project.add_commit(commit)
                is_newcomer = self.project.developers.add_from_commit(commit)
            else:
                raise CommitReleaseAlreadyAssigned(commit, self)

        self.commits.append(commit)
        self.developers.add_from_commit(commit, is_newcomer)

    def add_commits_from_pre_releases(self):
        """ This method is necessary for lazy loading commits """
        for pre_release in self.pre_releases:
            for commit in pre_release.commits:
                self.add_commit(commit, False)
            for newcomer in pre_release.developers.newcomers:
                self.developers.force_newcomer(newcomer)
            self.tail_commits += pre_release.tail_commits
            self.tail_commits = sorted(self.tail_commits, key=lambda commit: commit.author_time)

    def add_pre_release(self, pre_release: PreRelease):
        self.pre_releases.append(pre_release)
        self.commits.extend(pre_release.commits)


class PreRelease(Release):
    def __init__(self, project: Project, tag, release_type=None, prefix=None, major=None, minor=None, patch=None):
        super().__init__(project=project,
                         tag=tag,
                         release_type=release_type,
                         prefix=prefix,
                         major=major,
                         minor=minor,
                         patch=patch)

