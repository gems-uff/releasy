import pytest
import releasy
from releasy.repository import Repository
from releasy.miner_release import FinalReleaseMiner, ReleaseMiner
from releasy.project import Project
from .mock_repository import MockRepository, MockRepositoryProxy


class describe_release_miner:
    @pytest.fixture(autouse=True)
    def init(self):
        self.project = releasy.Miner(MockRepository()).apply(
            ReleaseMiner()
        ).mine()

    def it_mine_releases(self):
        assert len(self.project.releases) == 13
        assert self.project.releases['0.0.0-alpha1']
        assert self.project.releases['v0.9.0']
        assert self.project.releases['v1.0.0']
        assert self.project.releases['v1.0.2']
        assert self.project.releases['1.1.0']
        assert self.project.releases['1.1.1']
        assert self.project.releases['v2.0.0-beta1']
        assert self.project.releases['v2.0.0-alpha1']
        assert self.project.releases['v2.0.0']
        assert self.project.releases['2.0.0']
        assert self.project.releases['v2.0.1']
        assert self.project.releases['2.1.1pre']
        assert self.project.releases['v2.1.1']


class describe_final_release_miner:
    @pytest.fixture(autouse=True)
    def init(self):
        self.project = releasy.Miner(MockRepository()).apply(
            FinalReleaseMiner()
        ).mine()


    def it_mine_releases(self):
        assert len(self.project.releases) == 9
        assert self.project.releases['v0.9.0']
        assert self.project.releases['v1.0.0']
        assert self.project.releases['v1.0.2']
        assert self.project.releases['1.1.0']
        assert self.project.releases['1.1.1']
        assert self.project.releases['v2.0.0']
        assert self.project.releases['2.0.0']
        assert self.project.releases['v2.0.1']
        assert self.project.releases['v2.1.1']
