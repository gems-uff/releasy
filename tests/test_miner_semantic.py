import pytest
from datetime import timedelta

import releasy
from releasy.miner_release import FinalReleaseMiner
from releasy.miner_commit import HistoryCommitMiner
from releasy.miner_base_release import BaseReleaseMiner
from releasy.project import Project
from releasy.miner_semantic import SemanticReleaseMiner
from releasy.repository import Commit
from releasy.semantic import MainRelease, Patch, SReleaseSet

from .mock_repository import MockRepository

@pytest.fixture
def project() -> Project:
    project = releasy.Miner(MockRepository()).apply(
        FinalReleaseMiner(),
        HistoryCommitMiner(),
        BaseReleaseMiner(),
        SemanticReleaseMiner()
    ).mine()
    return project

@pytest.fixture
def mreleases(project: Project):
    return project.main_releases

@pytest.fixture
def patches(project: Project):
    return project.patches

class describe_release_miner:
    def it_mine_main_releases(self, mreleases: SReleaseSet[MainRelease]):
        assert len(mreleases) == 4
        assert mreleases['0.9.0'].releases.names == set(['v0.9.0'])
        assert mreleases['1.0.0'].releases.names == set(['v1.0.0'])
        assert mreleases['1.1.0'].releases.names == set(['1.1.0'])
        assert mreleases['2.0.0'].releases.names == set(['v2.0.0', '2.0.0'])

    def it_mine_main_release_patches(self, mreleases: SReleaseSet[MainRelease]):
        assert not mreleases['0.9.0'].patches
        assert mreleases['1.0.0'].patches.names == set(['1.0.2'])
        assert mreleases['1.1.0'].patches.names == set(['1.1.1'])
        assert mreleases['2.0.0'].patches.names == set(['2.0.1'])

    def it_mine_patches(self, patches: SReleaseSet[Patch]):
        assert len(patches) == 4
        assert patches['1.0.2'].releases.names == set(['v1.0.2'])
        assert patches['1.1.1'].releases.names == set(['1.1.1'])
        assert patches['2.0.1'].releases.names == set(['v2.0.1'])
        assert patches['2.1.1'].releases.names == set(['v2.1.1'])

    def it_mine_main_release_commits(self, project: Project, mreleases: SReleaseSet[MainRelease]):
        repo = project.repository
        assert mreleases['0.9.0'].commits \
            == set([Commit(repo, '0'), Commit(repo, '1')])
        assert mreleases['1.0.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '3')])
        assert mreleases['1.1.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '5'), Commit(repo, '6')])
        assert mreleases['2.0.0'].commits \
            == set([Commit(repo, '8'), Commit(repo, '9'), Commit(repo, '10'), 
                    Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'), 
                    Commit(repo, '14'),  Commit(repo, '15')])

    def it_mine_patches_commits(self, project: Project, patches: SReleaseSet[Patch]):
        repo = project.repository
        assert patches['1.0.2'].commits == set([Commit(repo, '13')])
        assert patches['1.1.1'].commits \
            == set([Commit(repo, '4'), Commit(repo, '7')])
        assert patches['2.0.1'].commits \
            == set([Commit(repo, '8'), Commit(repo, '9'), Commit(repo, '10'), 
                    Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'), 
                    Commit(repo, '14')])
        assert patches['2.1.1'].commits \
            == set([Commit(repo, '20'), Commit(repo, '19'), Commit(repo, '17'),
                    Commit(repo, '18'), Commit(repo, '16'),
                    Commit(repo, '10'), Commit(repo, '9'), Commit(repo, '8')])

    def it_mine_base_mreleases(self, mreleases: SReleaseSet[MainRelease]):
        assert not mreleases['0.9.0'].base_mreleases.names
        assert mreleases['1.0.0'].base_mreleases.names == set(['0.9.0'])
        assert mreleases['1.1.0'].base_mreleases.names == set(['0.9.0'])
        assert mreleases['2.0.0'].base_mreleases.names == set(
            ['0.9.0', '1.0.0', '1.1.0'])

    def it_mine_main_base_mrelease(self, mreleases: SReleaseSet[MainRelease]):
        assert not mreleases['0.9.0'].base_mrelease
        assert mreleases['1.0.0'].base_mrelease.name == '0.9.0'
        assert mreleases['1.1.0'].base_mrelease.name == '0.9.0'
        assert mreleases['2.0.0'].base_mrelease.name == '1.1.0'

    def it_mine_main_release_time(self, mreleases: SReleaseSet[MainRelease]):
        assert mreleases['0.9.0'].time \
            == MockRepository.ref_dt + timedelta(days=1)
        assert mreleases['1.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=3)
        assert mreleases['1.1.0'].time \
            == MockRepository.ref_dt + timedelta(days=6)
        assert mreleases['2.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=14)

    def it_mine_main_release_cycle(self, mreleases: SReleaseSet[MainRelease]):
        assert mreleases['0.9.0'].cycle == None
        assert mreleases['1.0.0'].cycle == timedelta(days=2)
        assert mreleases['1.1.0'].cycle == timedelta(days=5)
        assert mreleases['2.0.0'].cycle == timedelta(days=8)
