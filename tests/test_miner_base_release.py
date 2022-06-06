import pytest

import releasy
from releasy.miner_commit import HistoryCommitMiner
from releasy.miner_release import ReleaseMiner
from releasy.release import ReleaseSet
from releasy.project import Project
from releasy.miner_base_release import BaseReleaseMiner

from .mock_repository import MockRepository


@pytest.fixture
def project() -> Project:
    project = releasy.Miner(MockRepository()).apply(
        ReleaseMiner(), 
        HistoryCommitMiner(),
        BaseReleaseMiner()
    ).mine()
    return project

@pytest.fixture
def releases(project: Project):
    return project.releases
    
class describe_base_release_miner():
    def it_mine_base_releases(self, releases: ReleaseSet):
        assert not releases['0.0.0-alpha1'].base_releases
        assert releases['v0.9.0'].base_releases.names == set(['0.0.0-alpha1'])
        assert releases['v1.0.0'].base_releases.names == set(['v0.9.0'])
        assert releases['v1.0.2'].base_releases.names == set(['v1.0.0'])
        assert releases['1.1.0'].base_releases.names == set(['v0.9.0'])
        assert releases['1.1.1'].base_releases.names == set(['1.1.0', 'v1.0.0'])
        assert releases['v2.0.0-alpha1'].base_releases.names == set(['1.1.1'])
        assert releases['v2.0.0-beta1'].base_releases.names == set(
            ['v2.0.0-alpha1'])
        assert releases['v2.0.0'].base_releases.names == set(
            ['v1.0.2', 'v0.9.0', 'v2.0.0-beta1'])
        assert releases['v2.0.1'].base_releases \
            == releases['v2.0.0'].base_releases
        assert releases['2.0.0'].base_releases.names == set(
            ['v2.0.0', 'v2.0.1'])
        assert releases['2.1.1pre'].base_releases.names == set(
            ['v2.0.0', 'v2.0.1'])
        assert releases['v2.1.1'].base_releases.names == set(
            ['2.0.0', '2.1.1pre', 'v2.0.0-beta1'])
