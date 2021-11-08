"""
Add semantic to releases, i.e.:
  - Main releases
  - Pre releases
  - Patches
"""
from __future__ import annotations
from typing import Dict, List
from .release import TYPE_MAIN, TYPE_MAJOR, TYPE_PATCH, Release

class SemanticRelease:
    """Add semantic to a release"""
    def __init__(self, release: Release) -> None:
        self.release: Release = release
        release.semantic_reference = self

class MainRelease(SemanticRelease):
    """A feature release (major or minor)"""
    def __init__(self, release: Release) -> None:
        super().__init__(release)
        self.patches: Dict[str, Patch]= {} 

    def add_patch(self, patch: Patch):
        if patch and self.is_patch_compatible(patch):
            self.patches[patch.name] = patch
            patch.main_release = self

    def is_patch_compatible(self, patch: Patch):
        mrelease_version = self.release.version
        patch_version = patch.release.version
        if mrelease_version.numbers[0] == patch_version.numbers[0] \
                and mrelease_version.numbers[1] == patch_version.numbers[1]:
            return True
        return False

    @property
    def name(self) -> str:
        if self.release.version.type(TYPE_MAJOR):
            return f"{self.release.version.numbers[0]}.x.x"
        else:
            return f"{self.release.version.numbers[0]}.{self.release.version.numbers[1]}.x"

    @property
    def base_main_releases(self) -> List[MainRelease]:
        base_releases = {}
        for version, brelease in self.release.base_releases.items():
            semantic_brelease = brelease.semantic_reference
            if brelease.version.type(TYPE_MAIN) \
                    and self.release.version != brelease.version:
                base_releases[semantic_brelease.name] = semantic_brelease
            elif brelease.version.type(TYPE_PATCH) \
                    and self.release.version != semantic_brelease.main_release.release.version:
                semantic_brelease = brelease.semantic_reference.main_release
                base_releases[semantic_brelease.name] = semantic_brelease
        return base_releases


class Patch(SemanticRelease):
    def __init__(self, release: Release) -> None:
        super().__init__(release)
        self.main_release: MainRelease = None

    @property
    def name(self) -> str:
        return self.release.version.number

    @property
    def base_main_releases(self) -> Dict[str, Release]:
        base_releases = {}
        for version, brelease in self.release.base_releases.items():
            semantic_brelease = brelease.semantic_reference
            if brelease.version.type(TYPE_MAIN) \
                    and self.release.version != brelease.version:
                base_releases[semantic_brelease.name] = semantic_brelease
            elif brelease.version.type(TYPE_PATCH) \
                    and self.release.version != semantic_brelease.main_release.release.version:
                semantic_brelease = brelease.semantic_reference.main_release
                base_releases[semantic_brelease.name] = semantic_brelease
        return base_releases

        
