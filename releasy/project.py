"""
"""
from typing import List
from .metamodel import Datasource
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
        self.releases: ReleaseSet = ReleaseSet()
        self.main_releases = ReleaseSet()
        self.patches = ReleaseSet()
        self.pre_releases = ReleaseSet()

    def add_release(self, release: Release):
        self.releases.add(release)
        if release.version.type(TYPE_MAIN):
            self.main_releases.add(release)
        if release.version.type(TYPE_PATCH):
            self.patches.add(release)
        if release.version.type(TYPE_PATCH):
            self.patches.add(release) 
        if release.version.type(TYPE_PRE):
            self.pre_releases.add(release) 

    @property
    def prefixes(self) -> List[str]:
        prefixes = list(set(release.version.prefix for release in self.releases))
        return prefixes
