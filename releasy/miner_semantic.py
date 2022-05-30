from typing import Set
import re

from .miner_main import AbstractMiner, Project, Release, ReleaseSet
from .repository import Repository

class SemanticReleaseMiner(AbstractMiner):
    """
    Mine major, minor and main releases
    """
    def mine(self) -> Project:
        project = self.project

        
        for release in project.releases:
            pass

        return project
