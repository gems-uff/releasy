
from typing import Set

from releasy.release import Release
from releasy.old.version_format import ReleaseVersionFormat


class Miner:
    def __init__(self, repository) -> None:
        self.repository = repository

    def mine_release(self,
            releases: Set[Release], 
            version_format: ReleaseVersionFormat) -> Set[Release]:
        pass

    def mine_changes(self,
            releases: Set[Release], 
            strategy) -> Set[Release]:
        for release in releases:
            release.add_changes(strategy.assign(release))


