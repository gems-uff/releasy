from __future__ import annotations

from abc import ABCMeta

class ProjectFactory():
    strategy = None

    def __init__(self, strategy: MiningStrategy = None) -> None:
        if strategy == None:
            strategy = MiningStrategy.default()
        self.strategy = strategy

    def create(self, path: str) -> Project:
        """Create the project with all the releases"""
        project = Project()
        project.path = path



class MiningStrategy():
    vcs = None             # e.g., Git, Mock
    its = None             # e.g., GitHub Issues
    commitAssigment = None # e.g., HistoryBased
    issueAssigment = None
    
    @staticmethod
    def default():
        """ create default strategy """
        strategy = MiningStrategy()
        return strategy


class Project():
    path : str = None
    releases = None

