import pytest

from releasy.repository import Repository
from releasy.miner_main import Project
from releasy.miner_release import ReleaseMiner
from releasy.miner_commit import HistoryCommitMiner
from .mock_repository import MockRepositoryProxy

@pytest.fixture
def project():
    repository = Repository(MockRepositoryProxy())
    project = Project(repository)
    releaseMiner = ReleaseMiner(project)
    project = releaseMiner.mine()
    commitMiner = HistoryCommitMiner(project)
    project = commitMiner.mine()
    return project

class describe_history_commit_miner:
    def it_mine_commit(self, project: HistoryCommitMiner):
        release = project.release['v0.9.0']
        assert len(project.release['v0.9.0'].commits) == 1
        
        

