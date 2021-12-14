from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from releasy.miner import AbstractMiner

from releasy.release import ReleaseSet

from .release_miner import (
    AbstractReleaseMiner,
    AbstractReleaseSorter,
    Datasource,
    ReleaseMatcher,
    TagReleaseMiner,
    TimeReleaseSorter,
    VersionReleaseMatcher
)
from .commit_miner import HistoryCommitMiner

from ..miner_git import GitVcs
from .source import Vcs
from ..project import Project


class Miner:
    def __init__(self) -> None:
        self.strategy = MiningStrategy.default()
        self.params = {}
        self.datasource = None
        self.project = None
        self.init()

    def config(self, strategy: MiningStrategy):
        self.strategy = strategy

    def init(self) -> Miner:
        self.project = Project()
        self.datasource = Datasource()
        self.params = {}
        return self

    def vcs(self, vcs: object) -> Miner:
        if isinstance(vcs, str):
            self.datasource.vcs = GitVcs(vcs)
        elif isinstance(vcs, Vcs):
            self.datasource.vcs = vcs
        else:
            raise TypeError(vcs)
        return self

    def src(self, datasource: Datasource) -> Miner:
        self.datasource = datasource
        return self

    def config_params(self, params):
        self.params = params

    def mine_releases(self) -> Miner:
        release_miner = self.strategy.release_mine_strategy
        release_miner.matcher = self.strategy.release_match_strategy
        release_miner.sorter = self.strategy.release_sort_strategy
        releases = release_miner.mine_releases(self.datasource)
        self.project.releases = releases
        return self

    def mine_commits(self) -> Miner:
        commit_miner = self.strategy.commit_assigment_strategy
        releases = commit_miner.mine_commits(
            self.datasource,
            self.project.releases,
            self.params)
        return self

    def mine(self, miner: AbstractMiner, params: Dict[str, object] = None) -> Miner:
        mined_releases = miner.mine(self.project.releases, params)
        self.project.releases = mined_releases
        return self

    def create(self) -> Project:
        #TODO: Create project here
        return self.project


class MiningStrategy():
    vcs = None                                            # e.g., Git, Mock
    its = None                                            # e.g., GitHub Issues
    release_mine_strategy : AbstractReleaseMiner = None   # e.g., Tag
    release_match_strategy : ReleaseMatcher = None        # e.g., Version
    release_sort_strategy: AbstractReleaseSorter = None   # e.g., Time
    commit_assigment_strategy = None                      # e.g., HistoryBased
    issue_assigment_strategy = None                       # e.g., Commit Id

    @staticmethod
    def default():
        """ create default strategy """
        strategy = MiningStrategy()
        strategy.release_mine_strategy = TagReleaseMiner()
        strategy.release_match_strategy = VersionReleaseMatcher()
        strategy.release_sort_strategy = TimeReleaseSorter()
        strategy.commit_assigment_strategy = HistoryCommitMiner()
        return strategy
