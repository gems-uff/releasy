from __future__ import annotations

from .miner import (
    AbstractReleaseMiner,
    AbstractReleaseSorter,
    Datasource,
    HistoryCommitMiner,
    ReleaseMatcher,
    TagReleaseMiner,
    TimeReleaseSorter,
    VersionReleaseMatcher
)
from .miner_git import GitVcs
from .metamodel import Vcs
from .project import Project

class ProjectMiner():
    strategy = None

    def __init__(self, strategy: MiningStrategy = None) -> None:
        if strategy is None:
            strategy = MiningStrategy.default()
        self.strategy = strategy

    def mine(self, datasource: Datasource, **kwargs) -> Project:
        """Create the project with all the releases"""
        #vcs_params = [param for param in ]

        params = kwargs

        release_miner = self.strategy.release_mine_strategy
        release_miner.matcher = self.strategy.release_match_strategy
        release_miner.sorter = self.strategy.release_sort_strategy

        if 'vcs' not in params and 'path' in params:
            datasource.vcs = GitVcs(params['path'])

        releases = release_miner.mine_releases(datasource)

        commit_miner = self.strategy.commit_assigment_strategy
        releases = commit_miner.mine_commits(datasource, releases, params)

        project = Project()
        project.releases = releases
        project.datasource = datasource

        return project


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
