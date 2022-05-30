


from __future__ import annotations
from typing import Set
from .release import Project, Release
from .collection import ReleaseSet

class MainRelease:
    def __init__(self, project: Project, name: str, releases: Set[Release],
                 pre_releases: Set[Release], patches: Set[Release]) -> None:
        self.project = project
        self.name = name
        self.releases = ReleaseSet(releases)
        self.pre_releases = ReleaseSet(pre_releases)
        self.patches = ReleaseSet(patches)
