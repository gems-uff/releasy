from __future__ import annotations

from abc import ABCMeta

from releasy.data import Vcs

from .miner import AbstractReleaseMiner, PathCommitMiner, ReleaseMatcher, TagReleaseMiner, TimeVersionReleaseSorter, VersionReleaseMatcher
from .metamodel import Project

class ProjectFactory():
    strategy = None

    def __init__(self, strategy: MiningStrategy = None) -> None:
        if strategy is None:
            strategy = MiningStrategy.default()
        self.strategy = strategy

    def create(self, **kwargs) -> Project:
        """Create the project with all the releases"""
        #vcs_params = [param for param in ]
        vcs_factory_params = dict([(param,kwargs[param]) for param in kwargs])
        vcs = self.strategy.vcs_factory.create(vcs_factory_params)

        project_src = dict(
            vcs = vcs
        )

        release_miner = TagReleaseMiner(
            vcs,
            self.strategy.release_match_strategy
        )

        releases = release_miner.mine_releases()
        releases_wbases = self.strategy.release_sort_strategy.sort(releases)

        releases = release_miner.mine_releases()
        commit_miner = PathCommitMiner(vcs, releases)
        releases = commit_miner.mine_commits()

        project = Project()
        project.releases = releases

        return project


class MiningStrategy():
    vcs_factory : VcsFactory = None                       # e.g., Git, Mock
    its_factory = None                                    # e.g., GitHub Issues
    release_source_strategy : AbstractReleaseMiner = None # e.g., Tag
    release_match_strategy : ReleaseMatcher = None        # e.g., Version
    release_sort_strategy = TimeVersionReleaseSorter()    # e.g., Time
    commit_assigment_strategy = None                      # e.g., HistoryBased
    issue_assigment_strategy = None                       # e.g., Commit Id

    @staticmethod
    def default():
        """ create default strategy """
        strategy = MiningStrategy()
        strategy.vcs_factory = GitVcsFactory()
        # strategy.release_source_strategy = TagReleaseMiner()
        strategy.release_match_strategy = VersionReleaseMatcher()
        strategy.release_sort_strategy = TimeVersionReleaseSorter()
        return strategy


class VcsFactory():
    def create(self, params) -> Vcs:
        pass


class GitVcsFactory(VcsFactory):
    def create(self, params) -> Vcs:
        pass

