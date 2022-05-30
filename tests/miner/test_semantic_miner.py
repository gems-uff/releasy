
import pytest
from releasy.release_old import ReleaseSet
from releasy.miner.semantic_miner import OrphanSemanticMiner, SemanticMiner
from releasy.miner.factory import Miner
from ..mock import VcsMock


def describe_semantic_miner():
    @pytest.fixture
    def releases():
        miner = Miner()
        miner.vcs(VcsMock())
        miner.mine_releases()
        miner.mine_commits()
        miner.mine(SemanticMiner())
        project = miner.create()
        return project.releases

    def it_mine_main_releases(releases: ReleaseSet):
        assert len([release for release in releases 
                            if release.semantic.is_main_release()]) \
            == 4
        assert releases['v0.9.0'].semantic.is_main_release()
        assert releases['v1.0.0'].semantic.is_main_release()
        assert releases['1.1.0'].semantic.is_main_release()
        assert releases['v2.0.0'].semantic.is_main_release()

    def it_mine_patches(releases: ReleaseSet):
        assert len([release for release in releases 
                            if release.semantic.is_patch()]) \
            == 3
        assert releases['v1.0.2'].semantic.is_patch()
        assert releases['v2.0.1'].semantic.is_patch()
        assert releases['v2.1.1'].semantic.is_patch()

    def it_mine_pre_releases(releases: ReleaseSet):
        assert len([release for release in releases 
                            if release.semantic.is_pre_release()]) \
            == 3
        assert releases['0.0.0-alpha1'].semantic.is_pre_release()
        assert releases['v2.0.0-alpha1'].semantic.is_pre_release()
        assert releases['v2.0.0-beta1'].semantic.is_pre_release()

    def it_mine_base_sreleases(releases: ReleaseSet):
        pass


def describe_orphan_semantic_miner():
    @pytest.fixture
    def releases():
        miner = Miner()
        miner.vcs(VcsMock())
        miner.mine_releases()
        miner.mine_commits()
        miner.mine(SemanticMiner())
        miner.mine(OrphanSemanticMiner())
        project = miner.create()
        return project.releases

    def it_mine_orphan_main_releases(releases: ReleaseSet):
        assert len([release for release in releases 
                            if release.semantic.is_main_release()]) \
            == 5
        assert releases['v0.9.0'].semantic.is_main_release()
        assert releases['v1.0.0'].semantic.is_main_release()
        assert releases['1.1.0'].semantic.is_main_release()
        assert releases['v2.0.0'].semantic.is_main_release()
        assert releases['v2.1.1'].semantic.is_main_release()

    def it_remove_orphan_patches(releases: ReleaseSet):
        assert len([release for release in releases 
                            if release.semantic.is_patch()]) \
            == 2
        assert releases['v1.0.2'].semantic.is_patch()
        assert releases['v2.0.1'].semantic.is_patch()

    def it_remove_orphan_pre_releases(releases: ReleaseSet):
        assert len([release for release in releases 
                            if release.semantic.is_pre_release()]) \
            == 3
        assert releases['0.0.0-alpha1'].semantic.is_pre_release()
        assert releases['v2.0.0-alpha1'].semantic.is_pre_release()
        assert releases['v2.0.0-beta1'].semantic.is_pre_release()
        assert set(releases['v0.9.0'].semantic.pre_releases) \
            == set([releases['0.0.0-alpha1'].semantic])
