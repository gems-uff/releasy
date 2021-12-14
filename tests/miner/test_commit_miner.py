import pytest

from typing import List

from releasy.miner.factory import Miner
from releasy.miner.commit_miner import (
    CommitMiner)
from releasy.miner.source import Datasource, Vcs
from releasy.commit import Commit
from releasy.release import ReleaseSet

from ..mock import VcsMock

@pytest.fixture
def vcs() -> Vcs:
    return VcsMock()

@pytest.fixture
def commits(vcs: Vcs) -> List[Commit]:
    return vcs.commits()

@pytest.fixture
def releases(vcs: Vcs):
    miner = Miner()
    miner.src(Datasource(vcs=vcs))
    miner.mine_releases()
    miner.mine_commits()
    project = miner.create()
    return project.releases

def describe_commit_miner():
    def it_is_abstract():
        with pytest.raises(TypeError):
            CommitMiner()

def describe_history_miner():
    def it_mine_commits(releases: ReleaseSet, commits: List[Commit]):
        assert releases["v0.9.0"].commits \
               == set([commits[1], commits[0]])
        assert releases["v1.0.0"].commits \
               == set([commits[3], commits[2]])
        assert releases["v1.0.2"].commits \
               == set([commits[13]])
        assert releases["1.1.0"].commits \
               == set([commits[6], commits[5], commits[2]])
        assert releases["v2.0.0-alpha1"].commits \
               == set([commits[8], commits[7], commits[4]])
        assert releases["v2.0.0-beta1"].commits \
               == set([commits[10], commits[9]])
        assert releases["v2.0.0"].commits \
               == set([commits[14], commits[12], commits[11]])
        assert releases["v2.0.1"].commits == releases["v2.0.0"].commits
        assert releases["v2.1.1"].commits \
               == set([commits[20], commits[19], commits[17], commits[18],
                       commits[16], commits[15]])

    def it_identify_shared_commits(releases: ReleaseSet, commits: List[Commit]):
        assert not releases['v0.9.0'].has_shared_commits
        assert releases['v1.0.0'].has_shared_commits
        assert not releases['v1.0.2'].has_shared_commits
        assert releases['1.1.0'].has_shared_commits
        assert not releases['v2.0.0-alpha1'].has_shared_commits
        assert not releases['v2.0.0-beta1'].has_shared_commits
        assert releases['v2.0.0'].has_shared_commits
        assert releases['v2.0.1'].has_shared_commits
        assert not releases['v2.1.1'].has_shared_commits
        assert len(commits[14].releases) == 2
        assert len(commits[2].releases) == 2

    def it_mine_base_releases(releases):
        assert not releases['v0.9.0'].base_releases
        assert releases["v1.0.0"].base_releases \
               == set([releases['v0.9.0']])
        assert releases["v1.0.2"].base_releases \
               == set([releases['v1.0.0']])
        assert releases["1.1.0"].base_releases \
               == set([releases['v0.9.0']])
        assert releases["v2.0.0-alpha1"].base_releases \
               == set([releases['v1.0.0'], releases['1.1.0']])
        assert releases["v2.0.0-beta1"].base_releases \
               == set([releases['v2.0.0-alpha1']])
        assert releases["v2.0.0"].base_releases \
               == set([releases['v1.0.2'], releases['v2.0.0-beta1']])
        assert releases["v2.0.1"].base_releases \
               == releases["v2.0.0"].base_releases
        assert releases["v2.1.1"].base_releases \
               == set([releases['v2.0.0'], releases['v2.0.1'], releases['v2.0.0-beta1']])

    # def it_has_delay(releases: List[Release]):
    #     #TODO: release[0].delay
    #     assert releases[1].delay == datetime.timedelta(days=2)
    #     assert releases[2].delay == datetime.timedelta(days=10)
    #     assert releases[3].delay == datetime.timedelta(days=5)
    #     assert releases[4].delay == datetime.timedelta(days=2)
    #     assert releases[5].delay == datetime.timedelta(days=2)
    #     assert releases[6].delay == datetime.timedelta(days=4)
    #     assert releases[7].delay == datetime.timedelta(hours=1)
    #     assert releases[8].delay == datetime.timedelta(days=6)
       