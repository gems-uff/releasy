"""
"""

from .metamodel import (
    Datasource
)
from .release import (
    TYPE_MAIN,
    TYPE_MAJOR,
    TYPE_PATCH,
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

    def add_release(self, release: Release):
        self.releases.add(release)
        if release.version.type(TYPE_MAIN):
            self.main_releases.add(release)
        if release.version.type(TYPE_PATCH):
            self.patches.add(release)
