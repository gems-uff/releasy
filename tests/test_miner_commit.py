import pytest

import releasy
from releasy.project import Project
from releasy.miner_release import ReleaseMiner
from releasy.miner_commit import HistoryCommitMiner, MixedHistoryCommitMiner
from .mock_repository import MockRepository


class describe_mix_history_commit_miner:
    @pytest.fixture(autouse=True)
    def project(self) -> Project:
        project = releasy.Miner(MockRepository()).apply(
            ReleaseMiner(),
            MixedHistoryCommitMiner()
        ).mine()
        self.project = project

    def it_mine_commits(self):
        project = self.project
        assert project.releases['0.0.0-alpha1'].commits.ids == set(['0']) 
        assert project.releases['v0.9.0'].commits.ids == set(['1'])
        assert project.releases['v1.0.0'].commits.ids == set(['2', '3'])
        assert project.releases['r-1.0.2'].commits.ids == set(['13'])
        assert project.releases['1.1.0'].commits.ids == set(['2', '5', '6'])
        assert project.releases['1.1.1'].commits.ids == set(['4', '7'])
        assert project.releases['v2.0.0-alpha1'].commits.ids == set(['8'])
        assert project.releases['v2.0.0-beta1'].commits.ids == set(['9', '10'])
        assert project.releases['v2.0.0'].commits.ids == set(['2', '11', '12', '14'])
        assert project.releases['2.0'].commits.ids == set(['15'])
        assert project.releases['v2.0.0'].commits \
            == project.releases['v2.0.1'].commits
        assert project.releases['rel2.1.1pre'].commits.ids == set(['17'])
        assert project.releases['v2.1.1'].commits.ids \
            == set(['16', '18', '19', '20'])


class describe_history_commit_miner:
    @pytest.fixture(autouse=True)
    def project(self) -> Project:
        project = releasy.Miner(MockRepository()).apply(
            ReleaseMiner(),
            HistoryCommitMiner()
        ).mine()
        self.project = project

    def it_mine_commits(self):
        project = self.project
        assert project.releases['0.0.0-alpha1'].commits.ids == set(['0']) 
        assert project.releases['v0.9.0'].commits.ids == set(['1'])
        assert project.releases['v1.0.0'].commits.ids == set(['3', '2'])
        assert project.releases['1.1.0'].commits.ids == set(['6', '5'])
        assert project.releases['1.1.1'].commits.ids == set(['7', '4'])
        assert project.releases['v2.0.0-alpha1'].commits.ids == set(['8'])
        assert project.releases['v2.0.0-beta1'].commits.ids == set(['10', '9'])
        assert project.releases['r-1.0.2'].commits.ids == set(['13'])
        assert project.releases['v2.0.0'].commits.ids == set(['14', '12', '11'])
        assert project.releases['v2.0.1'].commits.ids == set(['14'])
        assert project.releases['2.0'].commits.ids == set(['15'])
        assert project.releases['rel2.1.1pre'].commits.ids == set(['17'])
        assert project.releases['v2.1.1'].commits.ids \
            == set(['20', '19', '18', '16'])


class describe_commit_set:
    @pytest.fixture(autouse=True)
    def project(self) -> Project:
        project = releasy.Miner(MockRepository()).apply(
            ReleaseMiner(),
            MixedHistoryCommitMiner()
        ).mine()
        self.project = project

    def it_has_authors(self):
        project = self.project
        assert project.releases['v0.9.0'].commits.authors \
            == set(['bob'])
        assert project.releases['1.1.1'].commits.authors \
            == set(['bob', 'alice'])
        assert project.releases['v2.0.0'].commits.authors \
            == set(['bob', 'alice'])
        assert project.releases['v2.1.1'].commits.authors \
            == set(['alice'])
    
    def it_has_committers(self):
        project = self.project
        assert project.releases['v0.9.0'].commits.committers \
            == set(['alice'])
        assert project.releases['1.1.1'].commits.committers \
            == set(['alice', 'charlie'])
        assert project.releases['v2.0.0'].commits.committers \
            == set(['bob', 'alice'])
        assert project.releases['v2.1.1'].commits.committers \
            == set(['alice'])
