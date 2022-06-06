from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Set

from releasy.project import Project

from .repository import Repository, Tag


class Miner:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
        self.project = Project()
    
    def mine(self, miner: AbstractMiner) -> Miner:
        mined_project = miner.mine(self.repository, self.project)
        self.project = mined_project
        return miner

    def project(self):
        return self.project


class AbstractMiner(ABC):
    def __init__(self) -> None:
        self.project: Project = None

    @abstractmethod
    def mine() -> Project:
        pass
