import pytest

from releasy.miner.factory import Miner
from releasy.miner.commit_miner import (
    CommitMiner)
from releasy.miner.source import (
    Datasource, 
    Vcs)
from ..mock import VcsMock

@pytest.fixture
def releases():
    miner = Miner()
    miner.src(Datasource(vcs=VcsMock()))
    miner.mine_releases()
    miner.mine_commits()
    project = miner.create()
    return project.releases

def describe_commit_miner():
    def it_is_abstract():
        with pytest.raises(TypeError):
            CommitMiner()

def describe_history_miner():
    def it_mine_commits(releases):
        assert len(releases["v1.0.0"].commits) == 2
        assert len(releases["v1.0.1"].commits) == 2
        assert len(releases["v1.0.2"].commits) == 1
        assert len(releases["v1.1.0"].commits) == 3
        assert len(releases["v2.0.0-alpha1"].commits) == 3
        assert len(releases["v2.0.0-beta1"].commits) == 2
        assert len(releases["v2.0.0"].commits) == 3
        assert len(releases["v2.0.1"].commits) == 3
        assert len(releases["v2.1.0"].commits) == 6

    def it_mine_base_releases(releases):
        assert not releases['v1.0.0'].base_releases
        assert "v1.0.0" in releases['v1.0.1'].base_releases
        assert "v1.0.1" in releases['v1.0.2'].base_releases
        assert "v1.0.0" in releases['v1.1.0'].base_releases
        assert "v1.1.0" in releases['v2.0.0-alpha1'].base_releases
        assert "v1.0.1" in releases['v2.0.0-alpha1'].base_releases
        assert "v2.0.0-alpha1" in releases['v2.0.0-beta1'].base_releases
        assert "v1.0.0" in releases['v2.0.0'].base_releases
        assert "v1.0.2" in releases['v2.0.0'].base_releases
        assert "v2.0.0-beta1" in releases['v2.0.0'].base_releases
        assert "v1.0.0" in releases['v2.0.1'].base_releases
        assert "v1.0.2" in releases['v2.0.1'].base_releases
        assert "v2.0.0-beta1" in releases['v2.0.1'].base_releases
        assert "v2.0.0-beta1" in releases['v2.1.0'].base_releases
        assert "v2.0.0" in releases['v2.1.0'].base_releases
