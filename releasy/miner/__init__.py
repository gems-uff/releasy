
from abc import ABC, abstractmethod
from typing import Dict

from ..project import Project
from ..release import ReleaseSet


class AbstractMiner(ABC):
    """ Abstract miner """
    @abstractmethod
    def mine(self, project: Project, params: Dict[str, object]) -> Project:
        pass

    #TODO add dependencies
