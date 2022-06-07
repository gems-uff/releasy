import pytest

import releasy
from releasy.project import Project
from releasy.miner_release import ReleaseMiner
from releasy.miner_commit import HistoryCommitMiner
from .mock_repository import MockRepository

@pytest.fixture
def project() -> Project:
    project = releasy.Miner(MockRepository()).apply(
        ReleaseMiner(),
        HistoryCommitMiner()
    ).mine()
    return project

class describe_history_commit_miner:
    def it_mine_commits(self, project: Project):
        assert project.releases['0.0.0-alpha1'].commits.ids == set(['0']) 
        assert project.releases['v0.9.0'].commits.ids == set(['1'])
        assert project.releases['v1.0.0'].commits.ids == set(['2', '3'])
        assert project.releases['v1.0.2'].commits.ids == set(['13'])
        assert project.releases['1.1.0'].commits.ids == set(['2', '5', '6'])
        assert project.releases['1.1.1'].commits.ids == set(['4', '7'])
        assert project.releases['v2.0.0-alpha1'].commits.ids == set(['8'])
        assert project.releases['v2.0.0-beta1'].commits.ids == set(['9', '10'])
        assert project.releases['v2.0.0'].commits.ids == set(['2', '11', '12', '14'])
        assert project.releases['2.0'].commits.ids == set(['15'])
        assert project.releases['v2.0.0'].commits \
            == project.releases['v2.0.1'].commits
        assert project.releases['2.1.1pre'].commits.ids == set(['17'])
        assert project.releases['v2.1.1'].commits.ids \
            == set(['16', '18', '19', '20'])