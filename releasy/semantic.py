"""
Add semantic to releases, i.e.:
  - Main releases
  - Pre releases
  - Patches
"""
from __future__ import annotations
import datetime
from typing import Dict, List
from .release import TYPE_MAIN, TYPE_MAJOR, TYPE_PATCH, Release, ReleaseVersion

class SemanticRelease:
    """Add semantic to a release"""
    def __init__(self, release: Release) -> None:
        self.release: Release = release
        release.sm_release = self

    def name(self) -> str:
        pass

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def base_main_releases(self) -> Dict[str, MainRelease]:
        base_main_releases = {}
        for name, base_release in self.release.base_releases.items():
            sm_base_release = base_release.sm_release
            if isinstance(sm_base_release, MainRelease):
                base_main_releases[sm_base_release.name] = sm_base_release
            else: # Patches or Pre releases
                base_main_releases[sm_base_release.main_release.name] \
                                    = sm_base_release.main_release

        if self.name in base_main_releases:
            del base_main_releases[self.name]
        return base_main_releases

    @property
    def version(self) -> ReleaseVersion:
        return self.release.version

    @property
    def time(self) -> datetime.datetime:
        return self.release.time

    @property
    def commits(self):
        """Main release commits"""
        return self.release.commits


class MainRelease(SemanticRelease):
    """A feature release (major or minor)"""
    def __init__(self, release: Release) -> None:
        super().__init__(release)
        self.patches: Dict[str, Patch]= {} 
        self.pre_releases: Dict[str, PreRelease]= {} 

    def add_patch(self, patch: Patch):
        if patch and self.is_patch_compatible(patch):
            self.patches[patch.name] = patch
            patch.main_release = self

    def add_pre_release(self, pre_release: PreRelease):
        if pre_release and self.is_pre_release_compatible(pre_release):
            self.pre_releases[pre_release.name] = pre_release
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
    def name(self) -> str:
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
            commits.add(pre_release.commits)
        return commits

    def __str__(self) -> str:
        return f"Main {self.name}"

    @property
    def base_main_releases(self) -> Dict[str, MainRelease]:
        base_main_releases = super().base_main_releases
        for name, pre_release in self.pre_releases.items():
            base_main_releases.update(pre_release.base_main_releases)
        
        if self.name in base_main_releases:
            del base_main_releases[self.name]
        return base_main_releases

    @property
    def base_main_release(self) -> MainRelease:
        if not self.base_main_releases:
            return None
        base_main_releases = [value for key, value \
                              in self.base_main_releases.items()]
        base_main_releases.append(self)
        sorted_base_main_releases = sorted(
            base_main_releases, 
            key = lambda main_release : main_release.release.version)
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
    def name(self) -> str:
        return self.release.version.number

    def __str__(self) -> str:
        return f"Patch {self.name}"


class PreRelease(SemanticRelease):
    def __init__(self, release: Release) -> None:
        super().__init__(release)

    @property
    def name(self) -> str:
        return f'{self.release.version.number}{self.release.version.suffix}'

    def __str__(self) -> str:
        return f"Pre {self.name}"
