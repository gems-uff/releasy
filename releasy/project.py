"""
"""
from typing import List

from .semantic import MainRelease, Patch, PreRelease
from .miner.source import Datasource
from .release import (
    TYPE_MAIN,
    TYPE_PATCH,
    TYPE_PRE,
    Release,
    ReleaseSet
)

class Project():
    """
    Represent a software project
    """

    def __init__(self) -> None:
        self.datasource: Datasource = None
        self._releases: ReleaseSet = ReleaseSet()
        self.main_releases = ReleaseSet()
        self.patches = ReleaseSet()
        self.pre_releases = ReleaseSet()

    @property
    def releases(self):
        return self._releases

    @releases.setter
    def releases(self, releases):
        for release in releases:
            self.add_release(release)

    #TODO: it could be optimized in the future
    def add_release(self, release: Release):
        self.releases.add(release)
        if release.version.type(TYPE_MAIN):
            main_release = MainRelease(release)
            self.main_releases.add(main_release)
            for patch in self.patches:
                main_release.add_patch(patch)
            for pre_release in self.pre_releases:
                main_release.add_pre_release(pre_release)
        if release.version.type(TYPE_PATCH):
            patch = Patch(release)
            self.patches.add(patch)
            for main_release in self.main_releases:
                main_release.add_patch(patch)
        if release.version.type(TYPE_PRE):
            pre_release = PreRelease(release)
            self.pre_releases.add(pre_release)
            for main_release in self.main_releases:
                main_release.add_pre_release(pre_release)

    @property
    def prefixes(self) -> List[str]:
        prefixes = list(set(release.version.prefix for release in self.releases))
        return prefixes
