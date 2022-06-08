from __future__ import annotations
from collections import OrderedDict
from typing import Callable, Dict, Generic, Iterator, Set, TypeVar
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from releasy.project import Project

import re
from datetime import datetime, timedelta

from .repository import (
    Commit,
    CommitSet, 
    Repository, 
    Tag)


class Release:
    def __init__(self, project: Project, name: str, tag: Tag) -> None:
        self.project = project
        self.name = name
        self.tag = tag
        if tag: #Fix must remove tag from release
            self.head = tag.commit
        self.commits = CommitSet()
        self.tails = set[Commit]()
        self.base_releases = ReleaseSet()
        self.version = ReleaseVersion(name)
    
    def __hash__(self):
        return hash((self.project, self.name))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Release):
            return self.project == __o.project and self.name == __o.name
        else:
            return False

    def __repr__(self) -> str:
        return self.name

    @property
    def time(self) -> datetime:
        return self.tag.time

    @property
    def merges(self):
        return CommitSet(
            commit for commit in self.commits if len(commit.parents) > 1)

    # @property
    # def cycle(self) -> timedelta:
    #     return 


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

    def is_main_release(self) -> bool:
        return self.type(TYPE_MAIN)

    def is_pre_release(self) -> bool:
        return self.type(TYPE_PRE)
    
    def is_major(self) -> bool:
        return self.type(TYPE_MAJOR)

    def is_minor(self) -> bool:
        return self.type(TYPE_MINOR)

    def is_patch(self) -> bool:
        return self.type(TYPE_PATCH)

    def type(self, mask: int) -> bool:
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


class ReleaseSet():
    def __init__(self, releases: Set[Release] = None) -> None:
        self._releases = OrderedDict[str, Release]()
        if releases:
            for release in releases:
                self.add(release)

    def __iter__(self) -> Iterator[Release]:
        return (release for release in self._releases.values())

    def __getitem__(self, key) -> Release:
        if isinstance(key, int):
            release_name = list(self._releases.keys())[key]
            return self._releases[release_name]
        elif isinstance(key, str):
            return self._releases[key]
        else:
            raise TypeError()

    def __contains__(self, item) -> bool:
        if isinstance(item, str) and item in self._releases:
            return True
        elif isinstance(item, Release) and item.name in self._releases:
            return True
        return False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ReleaseSet):
            return self._releases == __o._releases
        return False

    @property
    def names(self) -> Set[str]:
        """Return a set withh all release names"""
        return set(name for name in self._releases.keys())

    def first(self, func: Callable = None) -> Release:
        if self._releases:
            if func:
                ordered_releases = sorted(self._releases.values(), key=func)
            else:
                ordered_releases = list(self._releases.values())
            return ordered_releases[0]
        else:
            return None

    def last(self, func: Callable = None) -> Release:
        if self._releases:
            if func:
                ordered_releases = sorted(self._releases.values(), key=func)
            else:
                ordered_releases = list(self._releases.values())
            return ordered_releases[-1]
        else:
            return None

    @property
    def all(self) -> Set[Release]:
        return set(self._releases.values())

    def add(self, release: Release):
        if release:
            self._releases[release.name] = release

    def remove(self, release: Release):
        if release.name in self:
            del self._releases[release.name]

    def update(self, iterable):
        for item in iterable:
            self.add(item)

    def __len__(self):
        return len(self._releases)
