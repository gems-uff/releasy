from typing import Set
import pygit2

from releasy.release import Release
from releasy.old.version_format import ReleaseVersionFormat


class GitMiner:
    def __init__(self, path) -> None:
        self.path = path
        self._git = pygit2.Repository(path) 

    def mine_release(self,
            releases: Set[Release], 
            version_format: ReleaseVersionFormat) -> Set[Release]:
        pass

    def mine_changes(self,
            releases: Set[Release], 
            assignment_strategy) -> Set[Release]:
        pass


