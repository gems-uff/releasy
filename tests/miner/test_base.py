from typing import List
from datetime import datetime, timedelta

from releasy.miner.base import ReleaseMiner, Repository
from releasy.release2 import ReleaseReference


class MockRepository(Repository):
    def __init__(self, references) -> None:
        self._references = references

    @property
    def release_refs(self) -> List[ReleaseReference]:
        release_references = []
        timestamp = datetime(2024, 1, 1)
        for ref in self._references:
            release_reference = ReleaseReference(
                ref,
                timestamp,
                'Alice <alice@example.com>',
                f'{ref} description',
                []
            )
            release_references.append(release_reference)
            timestamp += timedelta(days=1)
        return release_references


class TestReleaseMiner:
    def it_mine_a_repository(self):
        repository = MockRepository(["1.0.0", "1.1.0"])
        release_miner = ReleaseMiner()
        releases = release_miner.mine(repository)

        assert releases[0].name == "1.0.0"
        assert releases[0].timestamp == datetime(2024, 1, 1)
        assert releases[0].developer == 'Alice <alice@example.com>'
        assert releases[0].description == "1.0.0 description"
        assert releases[1].name == "1.1.0"
        assert len(releases) == 2
    
    def it_skip_invalid_releases(self):
        repository = MockRepository(["1.0.0", "invalid", "1.1.0"])
        release_miner = ReleaseMiner()
        releases = release_miner.mine(repository)

        assert releases[0].name == "1.0.0"
        assert releases[1].name == "1.1.0"
        assert len(releases) == 2
    

