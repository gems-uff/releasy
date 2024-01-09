from abc import ABC, abstractmethod
from typing import List

from releasy.release2 import ReleaseReference


class Repository(ABC):
    """ The Repository is an abstraction of any repository that contains
    information about releases, its changes, issues, and collaborators"""

    @property
    @abstractmethod
    def release_refs(self) -> List[ReleaseReference]:
        """ The references to the releases """
        pass
