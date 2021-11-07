"""
"""
from __future__ import annotations
from typing import (List, Set)

import re

from .metamodel import ContributorTracker, FrequencySet, Tag
from .metamodel import Commit


class ReleaseSet:
    """ An easy form to retrieve releases. It contains a set of releases, 
    its commits, and base releases"""
    def __init__(self):
        self.index = {}
        self.releases : List[Release] = []

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.releases[key]
        elif isinstance(key, str):
            return self.releases[self.index[key]]
        else: 
            raise TypeError()

    def add(self, release: Release):
        self.releases.append(release)
        self.index[release.name] = len(self.releases)-1

    def add_all(self, releases: List[Release]):
        for release in releases:
            self.releases.append(release)
            self.index[release.name] = len(self.releases)-1

    def get_all(self):
        return self.releases

    @property
    def prefixes(self):
        """ return a set with all the release prefixes, including None if there
        is at least one release withou prefix """
        prefixes = FrequencySet()
        for release in self.releases:
            prefixes.add(release.name.prefix)
        return prefixes

    @property
    def suffixes(self):
        """ return a set with all the release suffixes """
        suffixes = FrequencySet()
        for release in self.releases:
            suffixes.add(release.name.suffix)
        return suffixes

    def __len__(self):
      return len(self.releases)

    def index_of(self, release: Release):
        return self.index[release.name]


class Release:
    """A software release"""

    def __init__(self, name: str, commit: Commit = None, time = None, description = None):
        self.name = name
        self.version = ReleaseVersion(name)
        self.head = commit
        self.time = time
        self.description = description
        self.commits: Set[Commit] = set([self.head])
        self.base_releases: Set[Release] = set()
        self.contributors : ContributorTracker = ContributorTracker()

    def __hash__(self):
        return hash((self.name, self.head))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        return False

    def __repr__(self):
        return repr(self.name)

    @property
    def merges(self):
        return set(commit for commit in self.commits if len(commit.parents) > 1)

    @property
    def main_base_release(self):
        if not self.base_releases:
            return None
            
        sorted_breleases = sorted(self.base_releases, 
                                  key = lambda release : release.name.version)
        return sorted_breleases[-1]


class TagRelease(Release):
    """ A release represented by a tag """

    def __init__(self, tag: Tag, name: ReleaseName):
        super().__init__(name, tag.commit, tag.time, None) #TODO add description
        self.tag = tag


class ReleaseName(str):
    """ Represent a release name, with prefix, version and suffix """
    def __init__(self, name: str, prefix: str = None, version: ReleaseVersion = None, suffix: str = None):
        if not name:
            raise ValueError("release name must have a non empty name")
        self.value = name
        self.prefix = prefix or None
        self.version = version or None
        self.suffix = suffix or None

    @property
    def semantic_version(self):
        """ Return 3 first version numbers separated by dot. Add 0 to missing 
        version and remove version number beyond 3 """
        
        version_sep = re.compile(r"[\._]")

        if not self.version:
            return None
        
        version_part = version_sep.split(self.version)
        version_part_cnt = len (version_part)

        for i in range(3 - version_part_cnt):
            version_part.append("0")
        return f"{version_part[0]}.{version_part[1]}.{version_part[2]}"

    def __new__(self, name, *args, **kwargs):
        return super().__new__(self, name)

    def __hash__(self):
        return hash(self.value)


TYPE_MAJOR   = 0b1100
TYPE_MINOR   = 0b0100
TYPE_MAIN    = 0b0100
TYPE_PATCH   = 0b0010
TYPE_PRE     = 0b0001
class ReleaseVersion():
    def __init__(self, name: str, separator: re.Pattern = None,
                 version_separator: re.Pattern = None) -> None:
        self.full_name = name
        self.prefix = None
        self.suffix = None
        
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
        #TODO sort pre releases
        return 0

    def type(self, mask: int):
        type = 0b0
        if self.suffix:
            type |= TYPE_PRE
        if int(self.numbers[2]) > 0:
            type |= TYPE_PATCH
        elif int(self.numbers[1]) > 0:
            type |= TYPE_MINOR
        elif int(self.numbers[0]) > 0:
            type |= TYPE_MAJOR
        
        if type & mask == mask:
            return True
        else:
            return False
