from __future__ import annotations

from abc import ABCMeta

from .miner import AbstractReleaseMiner, AbstractReleaseSorter, Datasource, HistoryCommitMiner, ReleaseMatcher, TagReleaseMiner, TimeReleaseSorter, TimeVersionReleaseSorter, VersionReleaseMatcher
from .metamodel import Project, Vcs

class ProjectFactory():
    strategy = None

    def __init__(self, strategy: MiningStrategy = None) -> None:
        if strategy is None:
            strategy = MiningStrategy.default()
        self.strategy = strategy

    def create(self, **kwargs) -> Project:
        """Create the project with all the releases"""
        #vcs_params = [param for param in ]

        params = kwargs
        vcs_factory_params = dict([(param,kwargs[param]) for param in kwargs])
        vcs = self.strategy.vcs_factory.create(vcs_factory_params)

        datasource = Datasource(
            vcs = vcs
        )

        release_miner = self.strategy.release_mine_strategy
        release_miner.matcher = self.strategy.release_match_strategy
        release_miner.sorter = self.strategy.release_sort_strategy

        releases = release_miner.mine_releases(datasource)

        commit_miner = self.strategy.commit_assigment_strategy
        releases = commit_miner.mine_commits(datasource, releases, params)

        project = Project()
        project.releases = releases

        return project


class MiningStrategy():
    vcs_factory : VcsFactory = None                       # e.g., Git, Mock
    its_factory = None                                    # e.g., GitHub Issues
    release_mine_strategy : AbstractReleaseMiner = None   # e.g., Tag
    release_match_strategy : ReleaseMatcher = None        # e.g., Version
    release_sort_strategy: AbstractReleaseSorter = None   # e.g., Time
    commit_assigment_strategy = None                      # e.g., HistoryBased
    issue_assigment_strategy = None                       # e.g., Commit Id

    @staticmethod
    def default():
        """ create default strategy """
        strategy = MiningStrategy()
        strategy.vcs_factory = GitVcsFactory()
        strategy.release_mine_strategy = TagReleaseMiner()
        strategy.release_match_strategy = VersionReleaseMatcher()
        strategy.release_sort_strategy = TimeReleaseSorter()
        strategy.commit_assigment_strategy = HistoryCommitMiner()
        return strategy


class VcsFactory():
    def create(self, params) -> Vcs:
        pass


class GitVcsFactory(VcsFactory):
    def create(self, params) -> Vcs:
        pass

