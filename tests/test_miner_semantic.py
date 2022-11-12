import pytest
from datetime import timedelta

import releasy
from releasy.miner_release import FinalReleaseMiner
from releasy.miner_commit import HistoryCommitMiner, MixedHistoryCommitMiner
from releasy.miner_base_release import BaseReleaseMiner
from releasy.miner_semantic import SemanticReleaseMiner
from releasy.repository import Commit

from .mock_repository import MockRepository


class describe_release_miner:
    @pytest.fixture(autouse=True)
    def project(self) -> None:
        project = releasy.Miner(MockRepository()).apply(
            FinalReleaseMiner(),
            HistoryCommitMiner(),
            BaseReleaseMiner(),
            SemanticReleaseMiner()
        ).mine()
        self.project = project

    def it_mine_main_releases(self):
        mreleases = self.project.main_releases
        assert len(mreleases) == 5
        assert mreleases['v0.9.0']
        assert mreleases['0.10.1']
        assert mreleases['v1.0.0']
        assert mreleases['1.1.0']
        assert mreleases['v2.0.0']

    def it_mine_patches(self):
        patches = self.project.patches
        assert len(patches) == 6
        assert patches['r-1.0.2']
        assert patches['1.1.1']
        assert patches['2.0']
        assert patches['v2.0.1']
        assert patches['v2.1.1']
        assert patches['v2.1.2']

    def it_mine_main_release_patches(self):
        mreleases = self.project.main_releases
        assert not mreleases['v0.9.0'].patches
        assert not mreleases['0.10.1'].patches
        assert mreleases['v1.0.0'].patches.names == set(['r-1.0.2'])
        assert mreleases['1.1.0'].patches.names == set(['1.1.1'])
        assert mreleases['v2.0.0'].patches.names \
            == set(['v2.0.1', '2.0', 'v2.1.1', 'v2.1.2'])

    def it_mine_main_release_commits(self):
        mreleases = self.project.main_releases
        assert mreleases['v0.9.0'].commits.ids == set(['1', '0'])
        assert mreleases['0.10.1'].commits.ids == set(['5'])
        assert mreleases['v1.0.0'].commits.ids == set(['3', '2'])
        assert mreleases['1.1.0'].commits.ids == set(['6'])
        assert mreleases['v2.0.0'].commits.ids \
            == set(['14', '12', '11', '10', '9', '8']) 

    def it_mine_patches_commits(self):
        patches = self.project.patches
        assert patches['r-1.0.2'].commits.ids == set(['13'])
        assert patches['1.1.1'].commits.ids == set(['7', '4'])
        assert patches['2.0'].commits.ids == set(['15'])
        assert patches['v2.0.1'].commits.ids == set()
        assert patches['v2.1.1'].commits.ids == \
            set(['19', '17'])
        assert patches['v2.1.2'].commits.ids == \
            set(['20', '18', '16'])

    def it_mine_base_mreleases(self):
        mreleases = self.project.main_releases
        assert not mreleases['v0.9.0'].main_base_release
        assert not mreleases['0.10.1'].main_base_release
        assert mreleases['v1.0.0'].main_base_release.name == 'v0.9.0'
        assert mreleases['1.1.0'].main_base_release.name == 'v1.0.0'
        assert mreleases['v2.0.0'].main_base_release.name == '1.1.0'

    def it_mine_main_release_time(self):
        mreleases = self.project.main_releases
        assert mreleases['v0.9.0'].time \
            == MockRepository.ref_dt + timedelta(days=1)
        assert mreleases['0.10.1'].time \
            == MockRepository.ref_dt + timedelta(days=5)
        assert mreleases['v1.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=3)
        assert mreleases['1.1.0'].time \
            == MockRepository.ref_dt + timedelta(days=6)
        assert mreleases['v2.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=14)

    def it_mine_main_release_cycle(self):
        mreleases = self.project.main_releases
        #TODO test tag time
        assert mreleases['v0.9.0'].cycle == timedelta(days=1)
        assert mreleases['0.10.1'].cycle == timedelta(days=0)
        assert mreleases['v1.0.0'].cycle == timedelta(days=2)
        assert mreleases['1.1.0'].cycle == timedelta(days=3)
        assert mreleases['v2.0.0'].cycle == timedelta(days=8)

    def it_mine_main_release_delay(self):
        mreleases = self.project.main_releases
        assert mreleases['v0.9.0'].delay == timedelta(0)
        assert mreleases['0.10.1'].delay == timedelta(0)
        assert mreleases['v1.0.0'].delay == timedelta(days=1)
        assert mreleases['1.1.0'].delay == timedelta(days=3)
        assert mreleases['v2.0.0'].delay == timedelta(days=2)


# class describe_release_miner_mixed:
#     @pytest.fixture(autouse=True)
#     def project(self) -> None:
#         project = releasy.Miner(MockRepository()).apply(
#             FinalReleaseMiner(),
#             MixedHistoryCommitMiner(),
#             BaseReleaseMiner(),
#             SemanticReleaseMiner()
#         ).mine()
#         self.project = project

#     def it_mine_main_releases(self):
#         mreleases = self.project.main_releases
#         assert len(mreleases) == 4
#         assert mreleases['0.9.0'].releases.names == set(['v0.9.0'])
#         assert mreleases['1.0.0'].releases.names == set(['v1.0.0'])
#         assert mreleases['1.1.0'].releases.names == set(['1.1.0'])
#         assert mreleases['2.0.0'].releases.names == set(['v2.0.0', '2.0'])

#     def it_mine_main_release_patches(self):
#         mreleases = self.project.main_releases
#         assert not mreleases['0.9.0'].patches
#         assert mreleases['1.0.0'].patches.names == set(['1.0.2'])
#         assert mreleases['1.1.0'].patches.names == set(['1.1.1'])
#         assert mreleases['2.0.0'].patches.names == set(['2.0.1'])

#     def it_mine_patches(self):
#         patches = self.project.patches
#         assert len(patches) == 4
#         assert patches['1.0.2'].releases.names == set(['r-1.0.2'])
#         assert patches['1.1.1'].releases.names == set(['1.1.1'])
#         assert patches['2.0.1'].releases.names == set(['v2.0.1'])
#         assert patches['2.1.1'].releases.names == set(['v2.1.1'])

#     def it_mine_main_release_commits(self):
#         mreleases = self.project.main_releases
#         repo = self.project.repository
#         assert mreleases['0.9.0'].commits \
#             == set([Commit(repo, '0'), Commit(repo, '1')])
#         assert mreleases['1.0.0'].commits \
#             == set([Commit(repo, '2'), Commit(repo, '3')])
#         assert mreleases['1.1.0'].commits \
#             == set([Commit(repo, '2'), Commit(repo, '5'), Commit(repo, '6')])
#         assert mreleases['2.0.0'].commits \
#             == set([Commit(repo, '8'), Commit(repo, '9'), Commit(repo, '10'), 
#                     Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'), 
#                     Commit(repo, '14'),  Commit(repo, '15')])

#     def it_mine_patches_commits(self):
#         patches = self.project.patches
#         repo = self.project.repository
#         assert patches['1.0.2'].commits == set([Commit(repo, '13')])
#         assert patches['1.1.1'].commits \
#             == set([Commit(repo, '4'), Commit(repo, '7')])
#         assert patches['2.0.1'].commits \
#             == set([Commit(repo, '8'), Commit(repo, '9'), Commit(repo, '10'), 
#                     Commit(repo, '2'), Commit(repo, '11'), Commit(repo, '12'), 
#                     Commit(repo, '14')])
#         assert patches['2.1.1'].commits \
#             == set([Commit(repo, '20'), Commit(repo, '19'), Commit(repo, '17'),
#                     Commit(repo, '18'), Commit(repo, '16'),
#                     Commit(repo, '10'), Commit(repo, '9'), Commit(repo, '8')])

#     def it_mine_base_mreleases(self):
#         mreleases = self.project.main_releases
#         assert not mreleases['0.9.0'].base_mreleases.names
#         assert mreleases['1.0.0'].base_mreleases.names == set(['0.9.0'])
#         assert mreleases['1.1.0'].base_mreleases.names == set(['0.9.0'])
#         assert mreleases['2.0.0'].base_mreleases.names == set(
#             ['0.9.0', '1.0.0', '1.1.0'])

#     def it_mine_main_base_mrelease(self):
#         mreleases = self.project.main_releases
#         assert not mreleases['0.9.0'].base_mrelease
#         assert mreleases['1.0.0'].base_mrelease.name == '0.9.0'
#         assert mreleases['1.1.0'].base_mrelease.name == '0.9.0'
#         assert mreleases['2.0.0'].base_mrelease.name == '1.1.0'

#     def it_mine_main_release_time(self):
#         mreleases = self.project.main_releases
#         assert mreleases['0.9.0'].time \
#             == MockRepository.ref_dt + timedelta(days=1)
#         assert mreleases['1.0.0'].time \
#             == MockRepository.ref_dt + timedelta(days=3)
#         assert mreleases['1.1.0'].time \
#             == MockRepository.ref_dt + timedelta(days=6)
#         assert mreleases['2.0.0'].time \
#             == MockRepository.ref_dt + timedelta(days=14)

#     def it_mine_main_release_cycle(self):
#         mreleases = self.project.main_releases
#         assert mreleases['0.9.0'].cycle == None
#         assert mreleases['1.0.0'].cycle == timedelta(days=2)
#         assert mreleases['1.1.0'].cycle == timedelta(days=5)
#         assert mreleases['2.0.0'].cycle == timedelta(days=8)

#     def it_mine_main_release_delay(self):
#         mreleases = self.project.main_releases
#         assert mreleases['0.9.0'].delay == timedelta(0)
#         assert mreleases['1.0.0'].delay == timedelta(0)
#         assert mreleases['1.1.0'].delay == timedelta(0)
#         assert mreleases['2.0.0'].delay == timedelta(0)


class describe_semantic_release_set:
    @pytest.fixture(autouse=True)
    def project(self) -> None:
        project = releasy.Miner(MockRepository()).apply(
            FinalReleaseMiner(),
            MixedHistoryCommitMiner(),
            BaseReleaseMiner(),
            SemanticReleaseMiner()
        ).mine()
        self.project = project

    def it_has_commits(self):
        assert self.project.main_releases.commits().ids \
            == set(['15', '14', '12', '11', '2', '1', '0',
                    '10', '9', '8', '6', '5', '3'])
        assert self.project.patches.commits().ids \
            == set(['20', '19', '17', '14', '13', '12', '11', '2', '10', '9',
                    '8', '7', '4', '18', '16'])

