
from datetime import datetime, timedelta
from typing import List
from releasy.miner.base import Repository
from releasy.release2 import ReleaseReference


class MockRepository(Repository):
    def __init__(self, references) -> None:
        self._change_references = []
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

changes = [
    1,
    2,
    3,
    4
]


class DescribeChangeMiner:
    def it_mine_changes(self):
        repository = MockRepository(['1.0.0', '1.1.0'])