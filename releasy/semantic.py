"""
Add semantic to releases, i.e.:
  - Main releases
  - Pre releases
  - Patches
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import datetime
from typing import Dict, List, Set

from releasy.commit import Commit
from .release import TYPE_MAIN, TYPE_MAJOR, TYPE_PATCH, Developer, Release, ReleaseVersion


class SemanticRelease(ABC):
    """Add semantic to a release"""
    def __init__(self, release: Release) -> None:
        self.release: Release = release
        release.sm_release = self
        self._base_main_releases = SmReleaseSet()

    @abstractmethod
    def semantic_name(self) -> str:
        pass

    @property
    def name(self) -> str:
        return self.release.name

    def __hash__(self) -> int:
        return self.release.__hash__()

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.release.__eq__(other.release)
        
    def __repr__(self) -> str:
        return self.__str__()

    @property
    def base_main_releases(self) -> SmReleaseSet:
        if self._base_main_releases:
            return self._base_main_releases

        for b_release in self.release.base_releases:
            b_srelease = b_release.sm_release
            if isinstance(b_srelease, MainRelease):
                self._base_main_releases.add(b_srelease)
            else:
                # Patches or Pre releases
                if hasattr(b_srelease, 'main_release'): #FIXME releases without main
                    self._base_main_releases.add(b_srelease.main_release)

        b_srelease_to_remove = []
        b_sreleases_to_track = [b_srelease for b_srelease in self._base_main_releases]
        while b_sreleases_to_track:
            b_release = b_sreleases_to_track.pop()
            for bb_release in b_release.base_main_releases:
                if bb_release not in b_srelease_to_remove:
                    b_sreleases_to_track.append(bb_release)
                    b_srelease_to_remove.append(bb_release)

        for b_release in b_srelease_to_remove:
            self._base_main_releases.remove(b_release.name)

        return self._base_main_releases

    @property
    def version(self) -> ReleaseVersion:
        return self.release.version

    @property
    def time(self) -> datetime.datetime:
        return self.release.time

    #TODO: Add test to SM Release Commits
    @property
    def commits(self) -> Set[Commit]:
        """Release commits"""
        return self.release.commits

    @property
    def newcomers(self) -> Set[Developer]:
        """Release commits"""
        return self.release.newcomers


class MainRelease(SemanticRelease):
    """A feature release (major or minor)"""
    def __init__(self, release: Release) -> None:
        super().__init__(release)
        self.patches: SmReleaseSet = SmReleaseSet()
        self.pre_releases: SmReleaseSet = SmReleaseSet()

    def add_patch(self, patch: Patch):
        if patch and self.is_patch_compatible(patch):
            self.patches.add(patch)
            patch.main_release = self

    def add_pre_release(self, pre_release: PreRelease):
        if pre_release and self.is_pre_release_compatible(pre_release):
            self.pre_releases.add(pre_release)
            pre_release.main_release = self

    def is_patch_compatible(self, patch: Patch):
        mrelease_version = self.release.version
        patch_version = patch.release.version
        if mrelease_version.numbers[0] == patch_version.numbers[0] \
                and mrelease_version.numbers[1] == patch_version.numbers[1]:
            return True
        return False

    def is_pre_release_compatible(self, pre_release: PreRelease):
        if self.release.version.number == pre_release.release.version.number:
            return True
        return False

    @property
    def semantic_name(self) -> str:
        if self.release.version.type(TYPE_MAJOR):
            return f"{self.release.version.numbers[0]}.0.0"
        else:
            return f"{self.release.version.numbers[0]}.{self.release.version.numbers[1]}.0"

    @property
    def commits(self):
        """
        Main release commits, which also include the commits from its pre
        releases.
        """
        commits = super().commits
        for pre_release in self.pre_releases:
            commits.update(pre_release.commits)
        return commits

    @property
    def newcomers(self) -> Set[Developer]:
        newcomers = super().newcomers
        for pre_release in self.pre_releases:
            newcomers.update(pre_release.newcomers)
        return newcomers

    def __str__(self) -> str:
        return f"Main {self.name}"

    @property
    def base_main_releases(self) -> SmReleaseSet:
        if self._base_main_releases:
            return self._base_main_releases

        self._base_main_releases = super().base_main_releases
        for pre_release in self.pre_releases:
            self._base_main_releases.update(pre_release.base_main_releases)
        
        if self.name in self._base_main_releases:
            self._base_main_releases.remove(self.name)
        return self._base_main_releases

    @property
    def base_main_release(self) -> MainRelease:
        if not self.base_main_releases:
            return None
    
        b_sreleases = [b_srelease \
                              for b_srelease in self.base_main_releases]
        b_sreleases.append(self)
        sorted_base_main_releases = sorted(
            b_sreleases, 
            key = lambda srelease : srelease.release.version)
        self_release_index = sorted_base_main_releases.index(self)
        return sorted_base_main_releases[self_release_index-1]

    @property
    def delay(self) -> datetime.timedelta:
        """Time interval between the release and it base main release"""
        if self.base_main_release:
            return self.time - self.base_main_release.time


class Patch(SemanticRelease):
    def __init__(self, release: Release) -> None:
        super().__init__(release)
        self.main_release: MainRelease = None

    @property
    def semantic_name(self) -> str:
        return self.release.version.number

    def __str__(self) -> str:
        return f"Patch {self.name}"


class PreRelease(SemanticRelease):
    def __init__(self, release: Release) -> None:
        super().__init__(release)

    @property
    def semantic_name(self) -> str:
        return f'{self.release.version.number}{self.release.version.suffix}'

    def __str__(self) -> str:
        return f"Pre {self.name}"


# TODO: Merge with ReleaseSet
class  SmReleaseSet():
    def __init__(self, releases = None) -> None:
        self._releases: Dict[str, SemanticRelease] = {}
        if releases:
            for release in releases:
                self.add(release)

    def __getitem__(self, key) -> SemanticRelease:
        if isinstance(key, int):
            release_name = list(self._releases.keys())[key]
            return self._releases[release_name]
        elif isinstance(key, str):
            return self._releases[key]
        else:
            raise TypeError()

    def __contains__(self, item):
        if isinstance(item, str):
            if item in self._releases:
                return True
            return False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, SmReleaseSet):
            if self._releases == __o._releases:
                return True
        return False

    def add(self, release: SemanticRelease):
        if release:
            self._releases[release.name] = release

    def update(self, releases: List):
        for release in releases:
            self.add(release)

    def remove(self, name) -> None:
        if name in self._releases:
            del self._releases[name]

    def __len__(self):
        return len(self._releases)

    def __repr__(self) -> str:
        return '[' \
             + ', '.join([release.name for release in self._releases.values()]) \
             + ']'
