
import pytest
import releasy
from releasy.miner_commit import HistoryCommitMiner
from releasy.miner_contributor import ContributorMiner
from releasy.miner_release import ReleaseMiner

from releasy.release import Release
from tests.mock_repository import MockRepository

class describe_release_version:

    def it_normalizes_version_numbers(self):
        """normalizes version numbers"""
        v1 = Release(None, "1.2.3", None).version
        assert v1.normalize(1) == [1]
        assert v1.normalize(2) == [1, 2]
        assert v1.normalize(3) == [1, 2, 3]
        assert v1.normalize(4) == [1, 2, 3, 0]


    def it_calculates_diff_vector(self):
        """calculates diff"""
        v1 = Release(None, "1.0.0", None).version
        v2 = Release(None, "1.0.1", None).version
        result = v1.diff(v2)
        assert result == [0, 0, -1]

        v1 = Release(None, "2.0.0", None).version
        v2 = Release(None, "1.0.1", None).version
        result = v1.diff(v2)
        assert result == [1, 0, -1]


class TestRelease:
    class describe_with_history_commit_miner():
        @pytest.fixture(autouse=True)
        def init(self) -> None:
            project = releasy.Miner(MockRepository()).apply(
                ReleaseMiner(),
                HistoryCommitMiner(),
                ContributorMiner()
            ).mine()
            self.releases = project.releases

        def it_has_committers(self):
            assert len(self.releases['v1.0.0'].contributors.committers) == 1
            assert len(self.releases['1.1.1'].contributors.committers) == 2

        def it_has_authors(self):
            assert len(self.releases['v1.0.0'].contributors.authors) == 1
            assert len(self.releases['1.1.1'].contributors.authors) == 2

        def it_has_newcomers(self):
            assert len(self.releases['0.0.0-alpha1'].contributors.newcomers) == 0
            assert len(self.releases['v0.9.0'].contributors.newcomers) == 1
            assert len(self.releases['v1.0.0'].contributors.newcomers) == 0
            assert len(self.releases['1.1.1'].contributors.newcomers) == 0
            assert len(self.releases['v2.0.0-alpha1'].contributors.newcomers) == 1

        def it_has_top_contributors_by_top(self):
            #FIX order on draw
            assert self.releases['1.1.1'].contributors.top(1)[0][1] == 50
            assert self.releases['v2.0.0'].contributors.top(1) \
                == [('alice', 66)]
            assert self.releases['v2.0.0'].contributors.top() \
                == [('alice', 66), ('bob', 33)]
            assert self.releases['v2.1'].contributors.top(1) \
                == [('alice', 100)]
            assert self.releases['v2.1'].contributors.top(10) \
                == [('alice', 100)]

        def it_has_top_contributors_by_percent(self):
            assert self.releases['v2.0.0'].contributors.top(percent=50) \
                == [('alice', 66)]
            assert self.releases['v2.0.0'].contributors.top(percent=75) \
                == [('alice', 66), ('bob', 33)]
            assert self.releases['v2.0.0'].contributors.top(percent=100) \
                == [('alice', 66), ('bob', 33)]
            assert self.releases['v2.1'].contributors.top(percent=50) \
                == [('alice', 100)]
            assert self.releases['v2.1'].contributors.top(percent=100) \

        def test_contributors_commits(self):
            "it store the commits from a group of contributors"
            assert self.releases['2.0'].contributors.commits(['alice']).ids \
                == set(['15'])
            assert not self.releases['2.0'].contributors.commits(['bob']).ids
            assert self.releases['v2.0.0-beta1'].contributors.commits(['alice']).ids \
                == set(['10', '9'])
            assert self.releases['v2.0.0-beta1'].contributors.commits(['bob']).ids \
                == set(['9'])
            assert self.releases['v2.0.0-beta1'].contributors.commits(['alice', 'bob']).ids \
                == set(['10', '9'])
            