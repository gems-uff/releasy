#import releasy
#import releasy.mine_strategy
import pytest
from datetime import datetime

import releasy
from releasy.miner import *
from .mock import VcsMock

def test_release_matcher():
    release_matcher = ReleaseMatcher()
    with pytest.raises(NotImplementedError):
        release_matcher.parse(None)

#FIXME:
# def test_release_sorter():
#     releases = ReleaseSet()
#     releases.add(Release("A", None, None, None))
#     release_sorter = ReleaseSorter()
#     with pytest.raises(NotImplementedError):
#         release_sorter.sort(releases)

def test_release_mine_stratety():
    release_miner = AbstractReleaseMiner()
    with pytest.raises(NotImplementedError):
        release_miner.mine_releases(None)


def test_commit_mine_strategy():
    commit_miner = AbstractCommitMiner()
    with pytest.raises(NotImplementedError):
        commit_miner.mine_commits(None, None)

#FIXME:
# def test_true_release_matcher():
#     datasource = Datasource(vcs = VcsMock())
#     release_miner = TagReleaseMiner()
#     release_miner.matcher = TrueReleaseMatcher()
#     releases = release_miner.mine_releases(datasource)
#     assert len(releases) == 10


def test_version_release_matcher():
    datasource = Datasource(vcs = VcsMock())
    release_miner = TagReleaseMiner()
    release_miner.matcher = VersionReleaseMatcher()
    releases = release_miner.mine_releases(datasource)
    assert len(releases) == 9

#FIXME
# def test_version_wo_pre_release_matcher():
#     datasource = Datasource(vcs = VcsMock())
#     release_miner = TagReleaseMiner()
#     release_miner.matcher = VersionWoPreReleaseMatcher()
#     releases = release_miner.mine_releases(datasource)
#     assert len(releases) == 7

#FIXME
# def test_version_wo_pre_release_matcher2():
#     datasource = Datasource(vcs = VcsMock())
#     release_miner = TagReleaseMiner()
#     release_miner.matcher = VersionWoPreReleaseMatcher(suffix_exception="-alpha1")
#     releases = release_miner.mine_releases(datasource)
#     assert len(releases) == 8
#     assert releases["v2.0.0-alpha1"].name == "v2.0.0-alpha1"


def test_version_release_exception():
    datasource = Datasource(vcs = VcsMock())
    release_miner = TagReleaseMiner()
    release_miner.matcher = VersionReleaseMatcher(release_exceptions=["v2.0.0-alpha1"])
    releases = release_miner.mine_releases(datasource)
    assert len(releases) == 8


def test_time_release_sorter():
    datasource = Datasource(vcs = VcsMock())
    release_miner = TagReleaseMiner()
    release_miner.matcher = VersionReleaseMatcher()
    release_miner.sorter = TimeReleaseSorter()
    releases = release_miner.mine_releases(datasource)
    assert releases[0].name == 'v1.0.0'
    assert releases[1].name == 'v1.0.1'
    assert releases[2].name == 'v1.1.0'
    assert releases[3].name == 'v2.0.0-alpha1'
    assert releases[4].name == 'v2.0.0-beta1'
    assert releases[5].name == 'v1.0.2'
    assert releases[6].name == 'v2.0.0'
    assert releases[7].name == 'v2.0.1'
    assert releases[8].name == 'v2.1.0'


def test_time_release_sorter2():
    releases = ReleaseSet()
    releases.add(Release("1", None, datetime(2020, 1, 2, 12, 00), None))
    releases.add(Release("0", None, datetime(2020, 1, 1, 12, 00), None))
    release_sorter = TimeReleaseSorter()
    sorted_releases = release_sorter.sort(releases)
    assert releases[0].name == "1"
    assert sorted_releases[0].name == "0"


def test_version_release_sorter():
    datasource = Datasource(vcs = VcsMock())
    release_miner = TagReleaseMiner()
    release_miner.matcher = VersionReleaseMatcher()
    release_miner.sorter = VersionReleaseSorter()
    releases = release_miner.mine_releases(datasource)
    assert releases[0].name == 'v1.0.0'
    assert releases[1].name == 'v1.0.1'
    assert releases[2].name == 'v1.0.2'
    assert releases[3].name == 'v1.1.0'
    assert releases[4].name == 'v2.0.0-alpha1'
    assert releases[5].name == 'v2.0.0-beta1'
    assert releases[6].name == 'v2.0.0'
    assert releases[7].name == 'v2.0.1'
    assert releases[8].name == 'v2.1.0'


def test_version_release_sorter2():
    releases = ReleaseSet()
    releases.add(Release("v1.0.1", None, datetime(2020, 1, 2, 12, 00), None))
    releases.add(Release("1.0.1", None, datetime(2020, 1, 1, 12, 00), None))
    release_sorter = VersionReleaseSorter()
    sorted_releases = release_sorter.sort(releases)
    assert releases[0].name == "v1.0.1"
    assert sorted_releases[0].name == "1.0.1"


def test_time_mine_strategy():
    miner = releasy.Miner()
    miner.strategy.release_sort_strategy = VersionReleaseSorter()
    miner.strategy.commit_assigment_strategy = TimeCommitMiner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases

    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 1
    assert len(releases[3].commits) == 0
    assert len(releases[4].commits) == 2
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 4
    assert len(releases[7].commits) == 0
    assert len(releases[8].commits) == 6


def test_time_naive_mine_strategy():
    miner = releasy.Miner()
    miner.strategy.release_sort_strategy = VersionReleaseSorter()
    miner.strategy.commit_assigment_strategy = TimeNaiveCommitMiner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases

    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 10
    assert len(releases[3].commits) == 0
    assert len(releases[4].commits) == 2
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 4
    assert len(releases[7].commits) == 0
    assert len(releases[8].commits) == 6


def test_time_expert_mine_strategy():
    miner = releasy.Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    expert_releases = project.releases

    miner = releasy.Miner()
    miner.strategy.release_sort_strategy = VersionReleaseSorter()
    miner.strategy.commit_assigment_strategy = TimeExpertCommitMiner()
    project = miner.mine(Datasource(vcs=VcsMock()), 
                             expert_release_set = expert_releases)
    releases = project.releases

    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 1
    assert len(releases[3].commits) == 3
    assert len(releases[4].commits) == 5
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 4
    assert len(releases[7].commits) == 4
    assert len(releases[8].commits) == 6


def test_range_mine_strategy():
    miner = releasy.Miner()
    miner.strategy.release_sort_strategy = VersionReleaseSorter()
    miner.strategy.commit_assigment_strategy = RangeCommitMiner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases
    
    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 1
    assert len(releases[3].commits) == 2 # interesting case
    assert len(releases[4].commits) == 4
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 4
    assert len(releases[7].commits) == 0
    assert len(releases[8].commits) == 6


def test_time_mine_base_release():
    miner = releasy.Miner()
    miner.strategy.release_sort_strategy = VersionReleaseSorter()
    miner.strategy.commit_assigment_strategy = TimeCommitMiner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases

    assert not releases[0].base_releases
    assert releases[1].base_releases == [releases[0]]
    assert releases[2].base_releases == [releases[1]]
    assert releases[3].base_releases == [releases[2]]
    assert releases[4].base_releases == [releases[3]]
    assert releases[5].base_releases == [releases[4]]
    assert releases[6].base_releases == [releases[5]]
    assert releases[7].base_releases == [releases[6]]
    assert releases[8].base_releases == [releases[7]]


def test_range_mine_base_release():
    miner = releasy.Miner()
    miner.strategy.release_sort_strategy = VersionReleaseSorter()
    miner.strategy.commit_assigment_strategy = RangeCommitMiner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases

    assert not releases[0].base_releases
    assert releases[1].base_releases == [releases[0]]
    assert releases[2].base_releases == [releases[1]]
    assert releases[3].base_releases == [releases[2]]
    assert releases[4].base_releases == [releases[3]]
    assert releases[5].base_releases == [releases[4]]
    assert releases[6].base_releases == [releases[5]]
    assert releases[7].base_releases == [releases[6]]
    assert releases[8].base_releases == [releases[7]]


def test_count_repository_commits():
    vcs = VcsMock()
    assert len(vcs.commits()) == 22


def test_count_merges():
    miner = releasy.Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases

    assert len(releases["v1.0.0"].merges) == 0
    assert len(releases["v1.0.1"].merges) == 0
    assert len(releases["v1.0.2"].merges) == 0
    assert len(releases["v1.1.0"].merges) == 0
    assert len(releases["v2.0.0-alpha1"].merges) == 1
    assert len(releases["v2.0.0-beta1"].merges) == 0
    assert len(releases["v2.0.0"].merges) == 2
    assert len(releases["v2.0.1"].merges) == 2
    assert len(releases["v2.1.0"].merges) == 3


def test_base_releases():
    miner = releasy.Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases
    assert not releases["v1.0.0"].base_releases
    assert len(releases["v1.0.1"].base_releases) == 1
    assert len(releases["v1.0.2"].base_releases) == 1
    assert len(releases["v1.1.0"].base_releases) == 1
    assert len(releases["v2.0.0-alpha1"].base_releases) == 2
    assert len(releases["v2.0.0-beta1"].base_releases) == 1
    assert len(releases["v2.0.0"].base_releases) == 3
    assert len(releases["v2.0.1"].base_releases) == 3
    assert len(releases["v2.1.0"].base_releases) == 2

#FIXME
# def test_main_base_release():
#     miner = releasy.Miner()
#     project = miner.mine(Datasource(vcs=VcsMock()))
#     releases = project.releases
#     assert not releases["v1.0.0"].main_base_release
#     assert releases["v1.0.1"].main_base_release == releases["v1.0.0"]
#     assert releases["v1.0.2"].main_base_release == releases["v1.0.1"]
#     assert releases["v1.1.0"].main_base_release == releases["v1.0.1"]
#     assert releases["v2.0.0-alpha1"].main_base_release == releases["v1.1.0"]
#     assert releases["v2.0.0-beta1"].main_base_release == releases["v2.0.0-alpha1"]
#     assert releases["v2.0.0"].main_base_release == releases["v2.0.0-beta1"]
#     assert releases["v2.0.1"].main_base_release == releases["v2.0.0"]
#     assert releases["v2.1.0"].main_base_release == releases["v2.0.0"]

def describe_history_miner():
    def it_mine_commits():
        miner = releasy.Miner()
        project = miner.mine(Datasource(vcs=VcsMock()))
        releases = project.releases
        assert len(releases["v1.0.0"].commits) == 2
        assert len(releases["v1.0.1"].commits) == 2
        assert len(releases["v1.0.2"].commits) == 1
        assert len(releases["v1.1.0"].commits) == 3
        assert len(releases["v2.0.0-alpha1"].commits) == 3
        assert len(releases["v2.0.0-beta1"].commits) == 2
        assert len(releases["v2.0.0"].commits) == 3
        assert len(releases["v2.0.1"].commits) == 3
        assert len(releases["v2.1.0"].commits) == 6

    def it_mine_base_releases():
        miner = releasy.Miner()
        project = miner.mine(Datasource(vcs=VcsMock()))
        releases = project.releases
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
