from __future__ import annotations
from typing import Dict, Generic, Set, TypeVar
import re

from .repository import Commit, Repository, Tag


class Project:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
        self.main_releases = None
        self.patches = None

    @property
    def releases(self) -> Set[Release]:
        return set(self.release)

class Release:
    def __init__(self, project: Project, name: str, tag: Tag) -> None:
        self.project = project
        self.name = name
        self.tag = tag
        if tag: #Fix must remove tag from release
            self.head = tag.commit
        self.commits: Set[Commit] = set()
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



T = TypeVar('T')
class ReleaseSet(Generic[T]):
    def __init__(self, releases: Set[T] = None) -> None:
        self._releases: Dict[str, Set] = {}
        if releases:
            for release in releases:
                self.add(release)

    def __iter__(self):
        return (release for release in self._releases.values())

    def __getitem__(self, key) -> T:
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

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, ReleaseSet):
            return self._releases == __o._releases
        return False

    @property
    def names(self) -> Set[str]:
        """Return a set withh all release names"""
        return set(name for name in self._releases.keys())

    def add(self, release: T):
        if release:
            self._releases[release.name] = release

    def update(self, iterable):
        for item in iterable:
            self.add(item)

    def __len__(self):
        return len(self._releases)
