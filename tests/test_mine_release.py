import pytest
from releasy.repository import Repository
from releasy.miner_release import ReleaseMiner
from releasy.release import Project
from .mock_repository import MockRepositoryProxy

class describe_release_miner:
    @pytest.fixture(autouse=True)
    def init(self):
        project = Project(Repository(MockRepositoryProxy()))
        self.miner = ReleaseMiner(project)

    def it_mine_releases(self):
        project = self.miner.mine()
        assert len(project.releases) == 10
