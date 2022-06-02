import pytest
from releasy.repository import Commit, Repository
from releasy.miner_release import ReleaseMiner
from releasy.miner_commit import HistoryCommitMiner
from releasy.release import Project
from releasy.miner_semantic import SemanticReleaseMiner
from releasy.semantic import MainRelease, Patch, SReleaseSet
from releasy.collection import ReleaseSet
from .mock_repository import MockRepositoryProxy

@pytest.fixture
def project() -> Project:
    repository = Repository(MockRepositoryProxy())
    project = Project(repository)
    releaseMiner = ReleaseMiner(project)
    project = releaseMiner.mine()
    commitMiner = HistoryCommitMiner(project)
    project = commitMiner.mine()
    semanticMiner = SemanticReleaseMiner(project)
    project = semanticMiner.mine()
    return project

@pytest.fixture
def mreleases(project: Project):
    return project.main_releases

@pytest.fixture
def patches(project: Project):
    return project.patches

class describe_release_miner:
    def it_mine_main_releases(self, mreleases: SReleaseSet):
        assert len(mreleases) == 4
        assert mreleases['0.9.0']
        assert mreleases['1.0.0']
        assert mreleases['1.1.0']
        assert mreleases['2.0.0']
        assert len(mreleases['0.9.0'].releases) == 1
        assert len(mreleases['1.0.0'].releases) == 1
        assert len(mreleases['1.1.0'].releases) == 1
        assert len(mreleases['2.0.0'].releases) == 2

    def it_mine_main_release_patches(self, mreleases: SReleaseSet):
        assert not mreleases['0.9.0'].patches
        assert len(mreleases['1.0.0'].patches) == 1
        assert mreleases['1.0.0'].patches['1.0.2'] 
        assert not mreleases['1.1.0'].patches
        assert len(mreleases['2.0.0'].patches) == 1 
        assert mreleases['2.0.0'].patches['2.0.1'] 

    def it_mine_patches(self, patches: SReleaseSet):
        assert len(patches) == 3
        assert patches['1.0.2']
        assert patches['2.0.1']
        assert patches['2.1.1']
        assert len(patches['1.0.2'].releases) == 1
        assert len(patches['2.0.1'].releases) == 1
        assert len(patches['2.1.1'].releases) == 1

    # def it_mine_pre_releases(self, mreleases: SReleaseSet):
    #     assert not mreleases['0.9.0'].pre_releases
    #     assert not mreleases['1.0.0'].pre_releases
    #     assert not mreleases['1.1.0'].pre_releases
    #     assert len(mreleases['2.0.0'].pre_releases) == 2 
    #     assert mreleases['2.0.0'].pre_releases['v2.0.0-beta1'] # FIX remove 'v2.0.0-'
    #     assert mreleases['2.0.0'].pre_releases['v2.0.0-alpha1'] # FIX remove 'v2.0.0-'

    def it_mine_main_release_commits(self, project: Project, mreleases: SReleaseSet[MainRelease]):
        repo = project.repository
        assert mreleases['0.9.0'].commits \
            == set([Commit(repo, '1')])
        assert mreleases['1.0.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '3')])
        assert mreleases['1.1.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '5'), Commit(repo, '6')])
        assert mreleases['2.0.0'].commits \
            == set([Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'),
                    Commit(repo, '14'), Commit(repo, '15')])


    # def it_mine_patches_commits(self, project: Project, mreleases: SReleaseSet[MainRelease]):
    #     repo = project.repository
    #     assert patches['1.0.2'].commits \
    #         == set([Commit(repo, '13')])
    #     assert patches['2.0.1'].commits \
    #         == set([Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'),
    #                 Commit(repo, '14')])
    #     assert patches['2.1.1']