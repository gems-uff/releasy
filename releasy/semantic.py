


from __future__ import annotations
from typing import Set
from .release import Project, Release

class MainRelease:
    def __init__(self, project: Project, name: str, releases: Set[Release],
                 pre_releases: Set[Release], patches: Set[Release]) -> None:
        self.project = project
        self.name = name
        self.releases = releases
        self.pre_releases = pre_releases
        self.patches = patches
