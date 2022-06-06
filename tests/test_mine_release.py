import pytest
from releasy.repository import Repository
from releasy.miner_release import FinalReleaseMiner, ReleaseMiner
from releasy.release import Project
from .mock_repository import MockRepositoryProxy

class describe_release_miner:
    @pytest.fixture(autouse=True)
    def init(self):
        project = Project(Repository(MockRepositoryProxy()))
        self.miner = ReleaseMiner(project)

    def it_mine_releases(self):
        project = self.miner.mine()
        assert len(project.releases) == 12
        assert project.release['0.0.0-alpha1']
        assert project.release['v0.9.0']
        assert project.release['v1.0.0']
        assert project.release['v1.0.2']
        assert project.release['1.1.0']
        assert project.release['v2.0.0-beta1']
        assert project.release['v2.0.0-alpha1']
        assert project.release['v2.0.0']
        assert project.release['2.0.0']
        assert project.release['v2.0.1']
        assert project.release['v2.1.1pre']
        assert project.release['v2.1.1']


class describe_release_miner:
    @pytest.fixture(autouse=True)
    def init(self):
        project = Project(Repository(MockRepositoryProxy()))
        self.miner = FinalReleaseMiner(project)

    def it_mine_releases(self):
        project = self.miner.mine()
        assert len(project.releases) == 9
        assert project.release['v0.9.0']
        assert project.release['v1.0.0']
        assert project.release['v1.0.2']
        assert project.release['1.1.0']
        assert project.release['1.1.1']
        assert project.release['v2.0.0']
        assert project.release['2.0.0']
        assert project.release['v2.0.1']
        assert project.release['v2.1.1']
