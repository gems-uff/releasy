import pytest
from releasy.miner.collaborator_miner import NewcomerMiner
from releasy.miner.factory import Miner
from releasy.release import Developer, ReleaseSet
from tests.mock import DevMock, VcsMock


@pytest.fixture
def dev() -> DevMock:
    return DevMock()

def describe_collaborator_miner():
    @pytest.fixture
    def releases():
        miner = Miner()
        miner.vcs(VcsMock())
        miner.mine_releases()
        miner.mine_commits()
        miner.mine(NewcomerMiner())
        project = miner.create()
        return project.releases

    def it_mine_newcommers(releases: ReleaseSet, dev: DevMock):
        assert releases['v0.9.0'].newcomers == set([dev.alice, dev.bob])
        assert not releases['v1.0.0'].newcomers
        assert not releases['v1.0.2'].newcomers
        assert not releases['1.1.0'].newcomers
        assert releases['v2.0.0-alpha1'].newcomers == set([dev.charlie])
        assert not releases['v2.0.0-beta1'].newcomers
        assert not releases['v2.0.0'].newcomers
        assert not releases['v2.0.1'].newcomers
        assert not releases['v2.1.0'].newcomers
