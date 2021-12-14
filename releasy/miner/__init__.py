
from abc import ABC, abstractmethod
from typing import Dict
from ..release import ReleaseSet


class AbstractMiner(ABC):
    """ Abstract miner """
    @abstractmethod
    def mine(self, releases: ReleaseSet, params: Dict[str, object]) -> ReleaseSet:
        pass

