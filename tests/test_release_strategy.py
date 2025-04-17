

from datetime import datetime
from typing import List
from releasy.contributor import Contributor
from releasy.old.version_format import SemanticVersioningFormat
from releasy.old.repository import Repository
from releasy.strategy_release import ReferenceReleaseStrategy

class MockRepositoryA(Repository):
    def release_refs(self):
        ALICE = Contributor("ALICE")
        refs = [
             ("1.0.0", "A", ALICE, datetime(2024, 1, 1)),
             ("1.1.0", "C", ALICE, datetime(2024, 1, 1)),
             ("1.1.1", "E", ALICE, datetime(2024, 1, 1)),
             ("1.2.0", "F", ALICE, datetime(2024, 1, 1))
        ]
        for ref in refs:
            yield ref


class DescribeReferenceReleaseStrategy:
    def it_mine_releases(self):
        version_format = SemanticVersioningFormat()
        strategy = ReferenceReleaseStrategy(version_format)
        repository = MockRepositoryA()
        releases = strategy.assign(repository)
        assert len(releases) == 4
        assert releases[0].name == "1.0.0"
        assert releases[1].name == "1.1.0"
        assert releases[2].name == "1.1.1"
        assert releases[3].name == "1.2.0"
