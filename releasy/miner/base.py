from abc import ABC, abstractmethod
from typing import Self, Set

from releasy.project2 import Project
from releasy.release2 import Release


class AMiner(ABC):
    def mine():
        pass
    

class ReleaseMiner(AMiner):
    @abstractmethod
    def mine() -> Set[Release]:
        pass


class Miner:
    def __init__(self, path: str, project: Project = None) -> None:
        self.path = path
        self.project = project
        self.miners = []

    def apply(self) -> Self:
        return self
    
    def mine() -> Project:
        pass

# releasy.Miner("/", project)
#        .apply(GitMiner)
#        .apply(FinalReleaseOnly)
#        .apply(SemanticVersion)
#        .apply(HistoryBased)
#        .mine()
        