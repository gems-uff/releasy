"""
"""
from __future__ import annotations
from typing import (
    Dict,
    Generic,
    List,
    Set,
    TypeVar,
    TYPE_CHECKING)

import re

if TYPE_CHECKING:
    from .semantic import SemanticRelease

from .commit import (
    Commit,
    Tag)


class Release:
    """A software release"""

    def __init__(self, name: str, commit: Commit = None, time = None, description = None):
        self.name = name
        self.version = ReleaseVersion(name)
        self.head = commit
        self.time = time
        self.description = description
        self.commits: Set[Commit] = set()
        self.base_releases: Set[Release] = set()
        self.contributors : ContributorTracker = ContributorTracker()
        self.sm_release: SemanticRelease = None
        self.has_shared_commits: bool = False
        self.add_commit(commit)
        commit.head_releases.add(self)

    def __hash__(self):
        return hash((self.name, self.head))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        return False

    def __repr__(self):
        return repr(self.name)

    def add_commit(self, commit: Commit):
        """Add a commit to the release"""
        self._check_sharred_commmits(commit)
        self.commits.add(commit)
        commit.releases.add(self)

    def remove_commit(self, commit: Commit):
        self.commits.remove(commit)
        commit.releases.remove(self)

    def remove_base_release(self, release: Release):
        if release in self.base_releases:
            self.base_releases.remove(release)

    def _check_sharred_commmits(self, commit: Commit):
        if commit.releases:
            self.has_shared_commits = True
            for shared_release in commit.releases:
                shared_release.has_shared_commits = True

    @property
    def merges(self):
        return set(commit for commit in self.commits if len(commit.parents) > 1)

    @property
    def main_base_release(self):
        if not self.base_releases:
            return None
        breleases = [base_release for base_release in self.base_releases]
        breleases.append(self)
        sorted_breleases = sorted(breleases, 
                                  key = lambda release : release.version)
        self_release_index = sorted_breleases.index(self)
        return sorted_breleases[self_release_index-1]

    def add_base_release(self, release: Release):
        if release:
            self.base_releases.add(release)

    @property
    def delay(self):
        """Time interval between the release and it main base release"""
        if self.main_base_release:
            return self.time - self.main_base_release.time

class TagRelease(Release):
    """ A release represented by a tag """

    def __init__(self, tag: Tag, name: str):
        super().__init__(name, tag.commit, tag.time, None) #TODO: add description
        self.tag = tag


TYPE_MAJOR   = 0b10000
TYPE_MINOR   = 0b01000
TYPE_MAIN    = 0b00100
TYPE_PRE     = 0b00010
TYPE_PATCH   = 0b00001
class ReleaseVersion():
    def __init__(self, name: str, separator: re.Pattern = None,
                 version_separator: re.Pattern = None) -> None:
        self.full_name = name
        self.prefix = ''
        self.suffix = ''
        
        if not separator:
            separator = re.compile(
                r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
            )
        parts = separator.match(name)
        if parts:
            if parts.group('prefix'):
                self.prefix = parts.group('prefix')
            if parts.group('suffix'):
                self.suffix = parts.group('suffix')
            if parts.group('version'):
                self.number = parts.group('version')

        if not version_separator:
            version_separator = re.compile(r'([0-9]+)')
        version_parts = version_separator.findall(self.number)
        self.numbers = [int(version_part) for version_part in version_parts]
        if len(self.numbers) == 1:
            self.numbers.append(0)
        if len(self.numbers) == 2:
            self.numbers.append(0)

    def __lt__(self, other):
        return self.__cmp(self, other) < 0
    def __gt__(self, other):
        return self.__cmp(self, other) > 0
    def __eq__(self, other):
        return self.__cmp(self, other) == 0
    def __le__(self, other):
        return self.__cmp(self, other) <= 0
    def __ge__(self, other):
        return self.__cmp(self, other) >= 0

    def __cmp(self, version_a: ReleaseVersion, version_b: ReleaseVersion) -> int:
        for vnumber_a, vnumber_b in zip(version_a.numbers, version_b.numbers):
            if vnumber_a > vnumber_b:
                return 1
            if vnumber_a < vnumber_b:
                return -1
        if not version_a.suffix and version_b.suffix:
            return 1
        elif version_a.suffix and not version_b.suffix:
            return -1

        if version_a.suffix and version_b.suffix:
            if version_a.suffix > version_b.suffix:
                return 1
            elif version_a.suffix < version_b.suffix:
                return -1

        return 0

    def type(self, mask: int):
        type = 0b0
        if int(self.numbers[2]) > 0:
            type |= TYPE_PATCH
        elif int(self.numbers[1]) > 0:
            type |= TYPE_MINOR
        elif int(self.numbers[0]) > 0:
            type |= TYPE_MAJOR

        if self.suffix:
            type |= TYPE_PRE
        elif not (type & TYPE_PATCH):
            type |= TYPE_MAIN

        if type & mask == mask:
            return True
        else:
            return False

# TODO: ReleaseSet must handle Releases and Semantic Releases. 
# Currently, it works because of duck typing
class ReleaseSet():
    def __init__(self, releases = None) -> None:
        self._releases: Dict[str, Release] = {}
        if releases: 
            for release in releases:
                self.add(release)

    def __getitem__(self, key) -> Release:
        if isinstance(key, int):
            release_name = list(self._releases.keys())[key]
            return self._releases[release_name]
        elif isinstance(key, str):
            return self._releases[key]
        else:
            raise TypeError()

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            if item in self._releases:
                return True
        return False

    def add(self, release: Release):
        if release:
            self._releases[release.name] = release

    def update(self, iterable):
        for item in iterable:
            self.add(item)

    def __len__(self):
        return len(self._releases)


class CommitBuilder():
    def __init__(self) -> None:
        self.commit: Commit = None

    def init(self):
        pass


class FrequencySet(set):
    def __init__(self):
        self._count = {}

    def add(self, value):
        super().add(value)
        if value not in self._count:
            self._count[value] = 1
        else:
            self._count[value] += 1

    def count(self, value):
        return self._count[value]

    def mode(self):
        max_count = 0
        max_value = None
        for value in self._count:
            if self._count[value] > max_count:
                max_count = self._count[value]
                max_value = value
        return max_value


class Developer:
    """
    Project Contributors

    Attributes:
        login: developer id
        name: developer name
        email: developer e-mail
    """

    def __init__(self, login, name, email):
        self.login = login
        self.name = name
        self.email = email

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, obj):
        if isinstance(obj, Developer):
            if self.login == obj.login:
                return True
        return False

    def __repr__(self):
        return self.login


class ContributorTracker():
    """ Track developers' contributions to a release """
    def __init__(self, tracked_contributors: ContributorTracker = None):
        self.authors = set()
        self.committers = set()
        self.newcomers = set()
        self.tracked_contributors = set()
        if tracked_contributors:
            self.tracked_contributors = tracked_contributors.tracked_contributors

    def track(self, commit: Commit):
        author = commit.author
        committer = commit.committer
        self.authors.add(author)
        self.committers.add(committer)
        if committer not in self.tracked_contributors:
            self.newcomers.add(committer)
            self.tracked_contributors.add(committer)
        if author not in self.tracked_contributors:
            self.newcomers.add(author)
            self.tracked_contributors.add(author)



