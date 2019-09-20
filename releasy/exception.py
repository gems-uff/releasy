from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .model import Commit
    from .release import Release

class CommitReleaseAlreadyAssigned(Exception):
    def __init__(self, commit: Commit, release: Release):
        super().__init__(f"Tryied to assign {commit} to {release}, but is already assigned to {commit.release}")
        self.commit = commit
        self.release = release
        
