from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .repository import Repository
    from .semantic import SReleaseSet, MainRelease, Patch
    from .release import ReleaseSet

class Project:
    def __init__(self, name: str, repository: Repository) -> None:
        self.repository = repository
        self.main_releases: SReleaseSet[MainRelease] = None
        self.patches: SReleaseSet[Patch] = None
        self.releases: ReleaseSet = None
        self.name = name
