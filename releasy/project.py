"""
"""

from .metamodel import (
    Datasource
)
from .release import (
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
        switch = {
            "MAJOR": lambda release: self.main_releases.add(release),
            "MINOR": lambda release: self.main_releases.add(release),
            "PATCH": lambda release: self.patches.add(release)
        }
        switch.get(release.type)(release)
