from __future__ import annotations
from typing import Set
from .release import Project, Release
from .collection import ReleaseSet


class SemanticRelease:
    def __init__(self, project: Project, name: str, releases: Set[Release]):
        self.project = project
        self.name = name
        self.releases = releases


class MainRelease(SemanticRelease):
    def __init__(self, project: Project, name: str, releases: Set[Release],
                 pre_releases: Set[Release], patches: Set[Release]) -> None:
        super().__init__(project, name, releases)
        self.pre_releases = ReleaseSet(pre_releases)
        self.patches = ReleaseSet(patches)


class Patch(SemanticRelease):
    def __init__(self, project: Project, name: str, releases: Set[Release]) -> None:
        super().__init__(project, name, releases)

    
class PreRelease(SemanticRelease):
    def __init__(self, project: Project, name: str, releases: Set[Release],
                 pre_releases: Set[Release], patches: Set[Release]) -> None:
        super().__init__(project, name, releases)
