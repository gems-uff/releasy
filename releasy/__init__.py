
from __future__ import annotations

__all__ = [
    'Miner',
    'Project',
    'ReleaseMiner',
    'FinalReleaseMiner',
    'ReleaseMiner',
    'BaseReleaseMiner',
    'SemanticReleaseMiner']

from .miner_release import *
from .miner_commit import *
from .miner_base_release import *
from .miner_semantic import *

from .metric import ReleaseMetric

from .project import Project
from .repository import Repository
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
            self.repository = Repository(GitRepository(repository))
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



class Metrify:
    def __init__(self, releases) -> None:
        self.releases = [release for release in releases]
        self.metric_values = dict[str, List]

    def measure(self, name: str, metric: ReleaseMetric) -> Metrify:
        values = list()
        for release in self.releases:
            value = metric.measure(release)
            values.append(value)
        self.metric_values[name] = values
        return self
