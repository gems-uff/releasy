import pytest

from typing import List

from releasy.commit import Commit
from releasy.miner.source import Datasource
from releasy.miner.factory import Miner
from releasy.release_old import ReleaseSet

from ..mock import VcsMock

@pytest.fixture
def commits() -> List[Commit]:
    return VcsMock().commits()

@pytest.fixture
def releases() -> ReleaseSet:
    miner = Miner()
    miner.src(Datasource(vcs=VcsMock()))
    miner.mine_releases()
    project = miner.create()
    return project.releases


def describe_tag_release_miner():
    def it_mine_releases(releases):
        assert len(releases) == 10

    def it_assign_the_head_commit(releases: ReleaseSet, commits: List[Commit]):
        assert releases['0.0.0-alpha1'].head == commits[0]
        assert releases['v0.9.0'].head == commits[1]
        assert releases['v1.0.0'].head == commits[3]
        assert releases['v1.0.2'].head == commits[13]
        assert releases['1.1.0'].head == commits[6]
        assert releases['v2.0.0-alpha1'].head == commits[8]
        assert releases['v2.0.0-beta1'].head == commits[10]
        assert releases['v2.0.0'].head == commits[14]
        assert releases['v2.0.1'].head == commits[14]
        assert releases['v2.1.1'].head == commits[20]
