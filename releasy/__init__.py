
from __future__ import annotations

__all__ = [
    'Miner',
    'Project',
    'ReleaseMiner',
    'FinalReleaseMiner',
    'HistoryCommitMiner',
    'MixedHistoryCommitMiner',
    'ContributorMiner',
    'BaseReleaseMiner',
    'SemanticReleaseMiner']

from .miner_release import *
from .miner_commit import *
from .miner_base_release import *
from .miner_contributor import *
from .miner_semantic import *

from .project import Project
from .repository import Repository
from .miner_base import AbstractMiner
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
    def __init__(self, repository: Repository, name: str = None) -> None:
        if isinstance(repository, str):
            self.repository = Repository(GitRepository(repository))
        else:
            self.repository = repository
        if name:
            self.name = name
        else:
            self.name = self.repository.name
        self.miners = list[AbstractMiner]()

    def apply(self, *miners) -> Miner:
        self.miners.extend(miners)
        return self

    def mine(self) -> Project:
        project = Project(self.name, self.repository)
        args = []
        for miner in self.miners:
            project, args = miner.mine(project, *args)
        return project
