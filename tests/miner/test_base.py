from typing import List

import re

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
        repository = MockRepository(['1.0.0', '1.1.0'])
        release_miner = ReleaseMiner()
        releases = release_miner.mine(repository)

        assert releases[0].name == '1.0.0'
        assert releases[0].timestamp == datetime(2024, 1, 1)
        assert releases[0].developer == 'Alice <alice@example.com>'
        assert releases[0].description == '1.0.0 description'
        assert releases[1].name == '1.1.0'
        assert len(releases) == 2
    
    def it_filter_references(self):
        repository = MockRepository(['1.0.0', '1.1.0-beta', '1.1.0'])
        release_miner = ReleaseMiner(
            reference_filter=lambda ref: re.fullmatch(r'\d+.\d+.\d+', ref.name)
        )
        releases = release_miner.mine(repository)

        assert len(releases) == 2
        assert releases[0].name == '1.0.0'
        assert releases[1].name == '1.1.0'

    def it_filter_releases(self):
        repository = MockRepository(['1.0.0', '1.1.0-beta', '1.1.0'])
        release_miner = ReleaseMiner(
            release_filter=lambda r: re.fullmatch(r'\d+.\d+.\d+', r.name)
        )
        releases = release_miner.mine(repository)

        assert len(releases) == 2
        assert releases[0].name == '1.0.0'
        assert releases[1].name == '1.1.0'

    def it_filter_invalid_releases(self):
        """ filter invalid releses
        Despite the absence of filter, the release_miner uses the
        SimpleVersioningSchema by default, which requires releases with numbers.
        Thus, 'invalid' is an invalid release name.
        """
        repository = MockRepository(['1.0.0', 'invalid', '1.1.0'])
        release_miner = ReleaseMiner()
        releases = release_miner.mine(repository)

        assert len(releases) == 2
        assert releases[0].name == '1.0.0'
        assert releases[1].name == '1.1.0'
