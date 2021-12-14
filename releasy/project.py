"""
"""
from typing import List, Set

from .semantic import (
    MainRelease,
    Patch,
    PreRelease,
    SmReleaseSet)
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
        self.releases: ReleaseSet = ReleaseSet()
        self.main_releases = SmReleaseSet()
        self.patches = SmReleaseSet()
        self.pre_releases = SmReleaseSet()

    @property
    def prefixes(self) -> Set[str]:
        prefixes = set(release.version.prefix for release in self.releases)
        return prefixes
