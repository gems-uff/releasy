import pytest
from releasy.repository import Repository
from releasy.miner_release import ReleaseMiner
from releasy.miner_commit import HistoryCommitMiner
from releasy.release import Project
from releasy.miner_semantic import SemanticReleaseMiner
from .mock_repository import MockRepositoryProxy

@pytest.fixture
def project():
    repository = Repository(MockRepositoryProxy())
    project = Project(repository)
    releaseMiner = ReleaseMiner(project)
    project = releaseMiner.mine()
    commitMiner = HistoryCommitMiner(project)
    project = commitMiner.mine()
    semanticMiner = SemanticReleaseMiner(project)
    project = semanticMiner.mine()
    return project


class describe_release_miner:
    def it_mine_releases(self, project: Project):
        assert len(project.releases) == 10
