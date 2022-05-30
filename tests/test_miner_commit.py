import pytest

from releasy.repository import Commit, Repository
from releasy.release import Project
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
    def it_mine_commit(self, project: Project):
        repo = project.repository
        release = project.release['v0.9.0']
        assert project.release['0.0.0-alpha1'].commits \
            == set([Commit(repo, '0')])
        assert project.release['v0.9.0'].commits \
            == set([Commit(repo, '1')])
        assert project.release['v1.0.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '3')])
        assert project.release['v1.0.2'].commits \
            == set([Commit(repo, '13')])
        assert project.release['1.1.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '5'), Commit(repo, '6')])
        assert project.release['v2.0.0-alpha1'].commits \
            == set([Commit(repo, '4'), Commit(repo, '7'), Commit(repo, '8')])
        assert project.release['v2.0.0-beta1'].commits \
            == set([Commit(repo, '9'), Commit(repo, '10')])
        assert project.release['v2.0.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'),
                    Commit(repo, '14')])
        assert project.release['v2.0.0'].commits \
            == project.release['v2.0.1'].commits
        assert project.release['v2.1.1'].commits \
            == set([Commit(repo, '15'), Commit(repo, '16'), Commit(repo, '17'),
                    Commit(repo, '18'), Commit(repo, '19'), Commit(repo, '20')])