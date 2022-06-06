
from __future__ import annotations

from releasy.project import Project

__all__ = ['Miner']

from .miner_main import AbstractMiner
from .repository_git import GitRepository

class Miner():
    """Wrapper to Releasy Miner implementations, e.g:
   
    project = releasy.Miner('repos/releasy').apply(
        FinalReleaseMiner(),
        HistoryCommitMiner(),
        BaseReleaseMiner(),
        SemanticReleaseMiner()
    ).mine()
    """
    def __init__(self, repository) -> None:
        if isinstance(repository, str):
            self.repository = GitRepository(repository)
        else:
            self.repository = repository
        self.miners = list[AbstractMiner]()

    def apply(self, *miners) -> Miner:
        self.miners.extend(miners)
        return self

    def mine(self) -> Project:
        project = Project(self.repository)
        for miner in self.miners:
            miner.project = project
            project = miner.mine()
        return project
