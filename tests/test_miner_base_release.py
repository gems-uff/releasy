import pytest

import releasy
from releasy.miner_commit import HistoryCommitMiner, MixedHistoryCommitMiner
from releasy.miner_release import ReleaseMiner
from releasy.release import ReleaseSet
from releasy.project import Project
from releasy.miner_base_release import BaseReleaseMiner

from .mock_repository import MockRepository


class describe_base_release_miner():
    @pytest.fixture(autouse=True)
    def project(self) -> Project:
        project = releasy.Miner(MockRepository()).apply(
            ReleaseMiner(), 
            MixedHistoryCommitMiner(),
            BaseReleaseMiner()
        ).mine()
        self.project = project

    def it_mine_base_releases(self):
        releases = self.project.releases
        assert not releases['0.0.0-alpha1'].base_releases
        assert releases['v0.9.0'].base_releases.names == set(['0.0.0-alpha1'])
        assert not releases['0.10.1'].base_releases
        assert releases['v1.0.0'].base_releases.names == set(['v0.9.0'])
        assert releases['r-1.0.2'].base_releases.names == set(['v1.0.0'])
        assert releases['1.1.0'].base_releases.names == set(['0.10.1', 'v0.9.0'])
        assert releases['1.1.1'].base_releases.names == set(['1.1.0', 'v1.0.0'])
        assert releases['v2.0.0-alpha1'].base_releases.names == set(['1.1.1'])
        assert releases['v2.0.0-beta1'].base_releases.names \
            == set(['v2.0.0-alpha1'])
        assert releases['v2.0.0'].base_releases.names == set(
            ['r-1.0.2', 'v0.9.0', 'v2.0.0-beta1'])
        assert releases['v2.0.1'].base_releases \
            == releases['v2.0.0'].base_releases
        assert releases['2.0'].base_releases.names == set(
            ['v2.0.0', 'v2.0.1'])
        assert releases['rel2.1.1pre'].base_releases.names == set(
            ['v2.0.0', 'v2.0.1'])
        assert releases['v2.1.1'].base_releases.names == set(['rel2.1.1pre'])
        assert releases['v2.1.2'].base_releases.names == set(
            ['v2.1.1', '2.0', 'v2.0.0-beta1'])


class describe_base_release_miner_with_history():
    @pytest.fixture(autouse=True)
    def project(self) -> Project:
        project = releasy.Miner(MockRepository()).apply(
            ReleaseMiner(), 
            HistoryCommitMiner(),
            BaseReleaseMiner()
        ).mine()
        self.project = project

    def it_mine_base_releases(self):
        releases = self.project.releases
        assert not releases['0.0.0-alpha1'].base_releases
        assert releases['v0.9.0'].base_releases.names == set(['0.0.0-alpha1'])
        assert not releases['0.10.1'].base_releases
        assert releases['v1.0.0'].base_releases.names == set(['v0.9.0'])
        assert releases['r-1.0.2'].base_releases.names == set(['v1.0.0'])
        assert releases['1.1.0'].base_releases.names == set(['v1.0.0', '0.10.1'])
        assert releases['1.1.1'].base_releases.names == set(['1.1.0', 'v1.0.0'])
        assert releases['v2.0.0-alpha1'].base_releases.names == set(['1.1.1'])
        assert releases['v2.0.0-beta1'].base_releases.names == set(
            ['v2.0.0-alpha1'])
        assert releases['v2.0.0'].base_releases.names == set(
            ['r-1.0.2', 'v1.0.0', 'v2.0.0-beta1'])
        assert releases['v2.0.1'].base_releases.names == set(['v2.0.0'])
        assert releases['2.0'].base_releases.names == set(
            ['v2.0.0', 'v2.0.1'])
        assert releases['v2.1.1'].base_releases.names == set(['rel2.1.1pre'])
        assert releases['v2.1.2'].base_releases.names == set(
            ['v2.1.1', '2.0', 'v2.0.0-beta1'])