from __future__ import annotations
from collections import OrderedDict

from typing import Callable, Generic, Iterator, Set, TypeVar

import datetime

from .project import Project
from .release import Release, ReleaseSet
from .repository import CommitSet


class SemanticRelease:
    def __init__(self, release: Release):
        self.project = release.project #TODO may be removed?
        self.release = release
        self.main_base_release: MainRelease = None
        self.base_release: SemanticRelease = None
        self.base_releases: SReleaseSet = SReleaseSet()
        self.prev_main_release = None
        
    @property
    def name(self):
        return self.release.name

    @property
    def commits(self):
        return self.release.commits
    
    def __hash__(self):
        return hash((self.project, self.name))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, SemanticRelease):
            return self.project == __o.project and self.name == __o.name
        else:
            return False

    def __repr__(self) -> str:
        return self.name

    # def __lt__(self, other):
    #     return self.release.version < other.release.version < 0
    # def __gt__(self, other):
    #     return self.release.version > other.release.version
    # def __le__(self, other):
    #     return self.release.version <= other.release.version
    # def __ge__(self, other):
    #     return self.release.version >= other.release.version

    @property
    def time(self) -> datetime.datetime:
        return self.release.time


class FinalRelease(SemanticRelease):
    pass

#TODO implement pre release logic
class PreRelease(SemanticRelease):
    pass


class MainRelease(SemanticRelease):
    def __init__(self, release: Release) -> None:
        super().__init__(release)
        self.patches = SReleaseSet()

    @property
    def cycle(self) -> datetime.timedelta:
        if self.prev_main_release:
            ref = self.prev_main_release.time
        elif self.commits:
            ref = self.commits.first(lambda c: c.author_time).author_time
        else:
            return datetime.timedelta(0)
        return self.time - ref

    @property
    def delay(self) -> datetime.timedelta:
        if self.prev_main_release and self.commits:
            ref = self.release.commits.first(
                lambda c: c.author_time).author_time
            return ref - self.prev_main_release.time
        else:
            return datetime.timedelta(0)


class Patch(FinalRelease):
    def __init__(self, release: Release) -> None:
        super().__init__(release)   
        self.main_release: MainRelease = None
        self.is_orphan = False
        self.was_main_release = False

    @property
    def cycle(self) -> datetime.timedelta:
        if self.base_release:
            ref = self.base_release.time
        else:
            ref = self.commits.first(lambda c: c.author_time).author_time
        return self.time - ref

    @property
    def delay(self) -> datetime.timedelta:
        if self.base_release:
            ref = self.release.commits.first(
                lambda c: c.author_time).author_time
            return ref - self.base_release.time
        else:
            return datetime.timedelta(0)


SR = TypeVar('SR')
class SReleaseSet(Generic[SR]):
    def __init__(self, sreleases: Set[SR] = None) -> None:
        self._sreleases = OrderedDict[str, SR]()
        if sreleases:
            for srelease in sreleases:
                self.add(srelease)

    def __len__(self) -> int:
        return len(self._sreleases)

    def __iter__(self) -> Iterator[SR]:
        return iter(self._sreleases.values())

    def __contains__(self, item) -> bool:
        if isinstance(item, str) and item in self._sreleases:
            return True
        elif isinstance(item, SemanticRelease) and item.name in self._sreleases:
            return True
        else:
            return False

    def __getitem__(self, key) -> SR:
        if isinstance(key, int):
            release_name = list(self._sreleases.keys())[key]
            return self._sreleases[release_name]
        elif isinstance(key, str):
            return self._sreleases[key]
        else:
            raise TypeError()

    def __repr__(self) -> str:
        return str(set(self._sreleases.keys()))

    def commits(self) -> CommitSet():
        commits = CommitSet()
        for srelease in self._sreleases.values():
            commits.update(srelease.commits)
        return commits

    @property
    def names(self) -> Set[str]:
        """Return a set with all release names"""
        return set(name for name in self._sreleases.keys())

    @property
    def all(self) -> Set[SR]:
        return set(self._sreleases.values())

    def prefixes(self) -> Set[str]:
        """Return a set with all the release prefixes"""
        prefixes = set[str]()
        for srelease in self._sreleases.values():
            for prefix in srelease.releases.prefixes():
                prefixes.add(prefix)
        return prefixes

    def first(self, func: Callable = None) -> SR:
        if self._sreleases:
            if func:
                ordered_sreleases = sorted(self._sreleases.values(), key=func)
            else:
                ordered_sreleases = list(self._sreleases.values())
            return ordered_sreleases[0]
        else:
            return None

    def last(self, func: Callable = None) -> SR:
        if self._sreleases:
            if func:
                ordered_sreleases = sorted(self._sreleases.values(), key=func)
            else:
                ordered_sreleases = list(self._sreleases.values())
            return ordered_sreleases[-1]
        else:
            return None

    def __or__(self, __o: SReleaseSet[SR]) -> SReleaseSet[SR]:
        sreleases = SReleaseSet[SR]()
        sreleases.update(self.all)
        sreleases.update(__o.all)
        return sreleases

    def add(self, srelease: SR) -> None:
        if srelease and srelease.name not in self._sreleases:
            self._sreleases[srelease.name] = srelease

    def update(self, sreleases: SR) -> None:
        for srelease in sreleases:
            self.add(srelease)
    
