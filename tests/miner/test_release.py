import pytest

from releasy.miner.source import Datasource
from releasy.miner.factory import Miner

from ..mock import VcsMock

@pytest.fixture
def releases():
    miner = Miner()
    miner.src(Datasource(vcs=VcsMock()))
    miner.mine_releases()
    project = miner.create()
    return project.releases


def describe_tag_release_miner():
    def it_mine_releases(releases):
        assert len(releases) == 9