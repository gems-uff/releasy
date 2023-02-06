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
        assert len(mreleases) == 7
        assert mreleases['v0.9.0']
        assert mreleases['v1.0.0']
        assert mreleases['1.1.0']
        assert mreleases['v2.0.0']
        assert mreleases['v2.1']
        assert mreleases['v3.1.0']
        assert mreleases['v4.0.0']

    def it_mine_patches(self):
        patches = self.project.patches
        assert len(patches) == 6
        assert patches['0.10.1']
        assert patches['r-1.0.2']
        assert patches['1.1.1']
        assert patches['2.0']
        assert patches['v2.0.1']
        assert patches['v3.1.1']

    def it_mine_main_release_patches(self):
        mreleases = self.project.main_releases
        assert not mreleases['v0.9.0'].patches
        assert mreleases['v1.0.0'].patches.names == set(['r-1.0.2'])
        assert mreleases['1.1.0'].patches.names == set(['1.1.1'])
        assert mreleases['v2.0.0'].patches.names \
            == set(['v2.0.1', '2.0', 'v3.1.1'])
        assert not mreleases['v2.1'].patches
        assert not mreleases['v4.0.0'].patches

    def it_mine_main_release_commits(self):
        mreleases = self.project.main_releases
        assert mreleases['v0.9.0'].commits.ids == set(['1', '0'])
        assert mreleases['v1.0.0'].commits.ids == set(['3', '2'])
        assert mreleases['1.1.0'].commits.ids == set(['6'])
        assert mreleases['v2.0.0'].commits.ids \
            == set(['14', '12', '11', '10', '9', '8']) 
        assert mreleases['v2.1'].commits.ids == set(['20', '18', '16'])
        assert mreleases['v3.1.0'].commits.ids == set(['22'])
        assert mreleases['v4.0.0'].commits.ids == set(['21'])
         
    def it_mine_patches_commits(self):
        patches = self.project.patches
        assert patches['0.10.1'].commits.ids == set(['5'])
        assert patches['r-1.0.2'].commits.ids == set(['13'])
        assert patches['1.1.1'].commits.ids == set(['7', '4'])
        assert patches['2.0'].commits.ids == set(['15'])
        assert patches['v2.0.1'].commits.ids == set()
        assert patches['v3.1.1'].commits.ids == \
            set(['19', '17'])

    def it_mine_base_mreleases(self):
        mreleases = self.project.main_releases
        assert not mreleases['v0.9.0'].main_base_release
        assert mreleases['v1.0.0'].main_base_release.name == 'v0.9.0'
        assert mreleases['1.1.0'].main_base_release.name == 'v1.0.0'
        assert mreleases['v2.0.0'].main_base_release.name == '1.1.0'
        assert mreleases['v2.1'].main_base_release.name == 'v2.0.0'
        assert mreleases['v3.1.0'].main_base_release.name == 'v2.1'
        assert mreleases['v4.0.0'].main_base_release.name == 'v2.0.0'

    def it_mines_previous_semantic_release(self):
        mreleases = self.project.main_releases
        assert not mreleases['v0.9.0'].prev_semantic_release
        assert mreleases['v1.0.0'].prev_semantic_release.name == 'v0.9.0'
        assert mreleases['1.1.0'].prev_semantic_release.name == 'v1.0.0'
        assert mreleases['v2.0.0'].prev_semantic_release.name == '1.1.0'
        assert mreleases['v2.1'].prev_semantic_release.name == 'v2.0.0'
        assert mreleases['v3.1.0'].prev_semantic_release.name == 'v2.1'
        assert mreleases['v4.0.0'].prev_semantic_release.name == 'v2.1'

    def it_mine_main_release_time(self):
        mreleases = self.project.main_releases
        assert mreleases['v0.9.0'].time \
            == MockRepository.ref_dt + timedelta(days=1)
        assert mreleases['v1.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=3)
        assert mreleases['1.1.0'].time \
            == MockRepository.ref_dt + timedelta(days=6)
        assert mreleases['v2.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=14)
        assert mreleases['v2.1'].time \
            == MockRepository.ref_dt + timedelta(days=20)
        assert mreleases['v3.1.0'].time \
            == MockRepository.ref_dt + timedelta(days=22)
        assert mreleases['v4.0.0'].time \
            == MockRepository.ref_dt + timedelta(days=21)

    def it_mine_main_release_cycle(self):
        mreleases = self.project.main_releases
        #TODO test tag time
        assert mreleases['v0.9.0'].cycle == timedelta(days=1)
        assert mreleases['v1.0.0'].cycle == timedelta(days=2)
        assert mreleases['1.1.0'].cycle == timedelta(days=3)
        assert mreleases['v2.0.0'].cycle == timedelta(days=8)
        assert mreleases['v2.1'].cycle == timedelta(days=6)
        assert mreleases['v3.1.0'].cycle == timedelta(days=2)
        assert mreleases['v4.0.0'].cycle == timedelta(days=1)

    # def it_mine_patch_cycle(self):
    #     patches = self.project.patches
    #     assert patches['r-1.0.2'].cycle == timedelta(days=10)
    #     assert patches['1.1.1'].cycle == timedelta(days=1)
    #     assert patches['2.0'].cycle == timedelta(days=1)
    #     assert patches['v2.0.1'].cycle == timedelta(days=0)
    #     assert patches['v2.1.1'].cycle == timedelta(days=4)
    #     assert patches['v2.1.2'].cycle == timedelta(days=1)

    def it_mine_main_release_delay(self):
        mreleases = self.project.main_releases
        assert mreleases['v0.9.0'].delay == timedelta(0)
        assert mreleases['v1.0.0'].delay == timedelta(days=1)
        assert mreleases['1.1.0'].delay == timedelta(days=3)
        assert mreleases['v2.0.0'].delay == timedelta(days=2)
        assert mreleases['v2.1'].delay == timedelta(days=2)
        assert mreleases['v3.1.0'].delay == timedelta(days=2)
        assert mreleases['v4.0.0'].delay == timedelta(days=1)

    def it_detects_orphan_releases(self):
        patches = self.project.patches
        orphan_patches = [patch for patch in patches if patch.is_orphan]
        assert len(orphan_patches) == 1
        assert orphan_patches[0].name == '0.10.1'
        
    def it_convert_duplicated_releases_to_patches(self):
        patches = self.project.patches
        dup_releases = [patch for patch in patches if patch.was_main_release]
        assert len(dup_releases) == 1
        assert dup_releases[0].name == '2.0'


class describe_semantic_release_set:
    @pytest.fixture(autouse=True)
    def project(self) -> None:
        project = releasy.Miner(MockRepository()).apply(
            FinalReleaseMiner(),
            HistoryCommitMiner(),
            BaseReleaseMiner(),
            SemanticReleaseMiner()
        ).mine()
        self.project = project

    def it_has_commits(self):
        assert self.project.main_releases.commits().ids \
            == set(['22', '21', '20', '18', '16', '14', '12', '11',
                    '2', '1', '0', '10', '9', '8', '6', '3'])
        assert self.project.patches.commits().ids \
            == set(['19', '17', '15', '13', '7', '5', '4'])

