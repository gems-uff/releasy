from __future__ import annotations

from typing import Dict, Generic, Set, TypeVar

import datetime

from .project import Project
from .release import Release, ReleaseSet
from .repository import CommitSet


class SemanticRelease:
    def __init__(self, project: Project, name: str, releases: ReleaseSet):
        self.project = project
        self.name = name
        self.releases = releases
        self.release: Release = None
        self.commits = CommitSet()
    
    def __hash__(self):
        return hash((self.project, self.name))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, SemanticRelease):
            return self.project == __o.project and self.name == __o.name
        else:
            return False

    def __repr__(self) -> str:
        return self.name

    def __lt__(self, other):
        return self.__cmp(other) < 0
    def __gt__(self, other):
        return self.__cmp(other) > 0
    def __eq__(self, other):
        return self.__cmp(other) == 0
    def __le__(self, other):
        return self.__cmp(other) <= 0
    def __ge__(self, other):
        return self.__cmp(other) >= 0

    def __cmp(self, __o: SemanticRelease) -> int:
        versions_a = [int(number) for number in self.name.split('.')]
        versions_b = [int(number) for number in __o.name.split('.')]
        for (version_a, version_b) in zip(versions_a, versions_b):
            if version_a > version_b:
                return 1
            if version_a < version_b:
                return -1
        return 0

    @property
    def time(self) -> datetime.datetime:
        return self.release.time

    @property
    def delay(self) -> datetime.timedelta:
        return self.release.time - self.commits[0].committer_time


class FinalRelease(SemanticRelease):
    pass

#TODO implement pre release logic
class PreRelease(SemanticRelease):
    pass


class MainRelease(FinalRelease):
    def __init__(self, project: Project, name: str, releases: ReleaseSet[Release],
                 patches: Set[Release]) -> None:
        super().__init__(project, name, releases)
        self.patches = SReleaseSet(patches)
        self.base_mreleases = SReleaseSet[MainRelease]()
        self.base_mrelease: MainRelease = None

    @property
    def cycle(self) -> datetime.timedelta:
        if self.base_mrelease:
            return self.time - self.base_mrelease.time
        else:
            return None

class Patch(FinalRelease):
    def __init__(self, project: Project, name: str, releases: ReleaseSet[Release]) -> None:
        super().__init__(project, name, releases)   
        self.main_release: MainRelease = None


SR = TypeVar('SR')
class SReleaseSet(Generic[SR]):
    def __init__(self, sreleases: Set[SR] = None) -> None:
        self._sreleases: Dict[str, SR] = dict()
        if sreleases:
            for srelease in sreleases:
                self.add(srelease)

    def __len__(self):
        return len(self._sreleases)

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

    @property
    def names(self) -> Set[str]:
        """Return a set with all release names"""
        return set(name for name in self._sreleases.keys())

    @property
    def all(self) -> Set[SR]:
        return set(self._sreleases.values())

    @property
    def first(self) -> SR:
        if self._sreleases:
            if len(self._sreleases) == 1:
                return self._sreleases[0]
            else:
                ordered_sreleases = sorted(self.all, key=lambda r: r.time)
                return ordered_sreleases[0]
        else:
            return None

    @property
    def last(self) -> SR:
        if self._sreleases:
            if len(self._sreleases) == 1:
                return self._sreleases[0]
            else:
                ordered_sreleases = sorted(self.all, key=lambda r: r.time)
                return ordered_sreleases[-1]
        else:
            return None

    def __or__(self, __o: SReleaseSet):
        sreleases = SReleaseSet()
        sreleases.update(self.all)
        sreleases.update(__o.all)
        return sreleases

    def add(self, srelease: SR):
        if srelease and srelease.name not in self._sreleases:
            self._sreleases[srelease.name] = srelease

    def update(self, sreleases: SR):
        for srelease in sreleases:
            self.add(srelease)

    def merge(self, srelease: SR):
        if srelease in self:
            name = srelease.name
            stored_srelease = self[name]

            for release in srelease.releases:
                if release not in stored_srelease.releases:
                    stored_srelease.releases.add(release)
        else:
            self.add(srelease)

    