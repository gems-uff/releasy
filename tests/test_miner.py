#import releasy
#import releasy.mine_strategy
import pytest
from datetime import datetime

from releasy.miner import *
from .mock import VcsMock


def test_release_matcher():
    release_matcher = ReleaseMatcher()
    with pytest.raises(NotImplementedError):
        release_matcher.parse(None)


def test_release_sorter():
    releases = ReleaseSet()
    releases.add(Release("A", None, None, None), None)
    release_sorter = ReleaseSorter()
    with pytest.raises(NotImplementedError):
        release_sorter.sort(releases)

def test_release_mine_stratety():
    release_miner = AbstractReleaseMiner(None, None, None)
    with pytest.raises(NotImplementedError):
        release_miner.mine_releases()


def test_commit_mine_strategy():
    commit_miner = AbstractCommitMiner(None, None)
    with pytest.raises(NotImplementedError):
        commit_miner.mine_commits()


def test_true_release_matcher():
    vcs = VcsMock()
    release_matcher = TrueReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    assert len(releases) == 10


def test_version_release_matcher():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    assert len(releases) == 9


def test_version_wo_pre_release_matcher():
    vcs = VcsMock()
    release_matcher = VersionWoPreReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    assert len(releases) == 7


def test_version_wo_pre_release_matcher2():
    vcs = VcsMock()
    release_matcher = VersionWoPreReleaseMatcher(suffix_exception="-alpha1")
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    assert len(releases) == 8
    assert releases[4].name == "v2.0.0-alpha1"


def test_time_release_sorter():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
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
    releases.add(Release("1", None, datetime(2020, 1, 2, 12, 00), None), None)
    releases.add(Release("0", None, datetime(2020, 1, 1, 12, 00), None), None)
    release_sorter = TimeReleaseSorter()
    sorted_releases = release_sorter.sort(releases)
    assert releases[0].name == "1"
    assert sorted_releases[0].name == "0"


def test_version_release_sorter():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
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
    releases.add(Release(ReleaseName("v1.0.1","v","1.0.1",None), None, datetime(2020, 1, 2, 12, 00), None), None)
    releases.add(Release(ReleaseName("1.0.1","","1.0.1",None), None, datetime(2020, 1, 1, 12, 00), None), None)
    release_sorter = VersionReleaseSorter()
    sorted_releases = release_sorter.sort(releases)
    assert releases[0].name == "v1.0.1"
    assert sorted_releases[0].name == "1.0.1"


def test_path_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = PathCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 1
    assert len(releases[3].commits) == 2 
    assert len(releases[4].commits) == 3
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 3
    assert len(releases[7].commits) == 0
    assert len(releases[8].commits) == 6


def test_time_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = TimeCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 10
    assert len(releases[3].commits) == 0
    assert len(releases[4].commits) == 2
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 4
    assert len(releases[7].commits) == 0
    assert len(releases[8].commits) == 6


def test_range_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = RangeCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 1
    assert len(releases[3].commits) == 2 # interesting case
    assert len(releases[4].commits) == 4
    assert len(releases[5].commits) == 2
    assert len(releases[6].commits) == 4
    assert len(releases[7].commits) == 0
    assert len(releases[8].commits) == 6


def test_path_mine_base_release():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = PathCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert not releases[0].base_releases
    assert len(releases[1].base_releases) == 1
    assert len(releases[2].base_releases) == 1
    assert len(releases[3].base_releases) == 1
    assert len(releases[4].base_releases) == 2
    assert len(releases[5].base_releases) == 1
    assert len(releases[6].base_releases) == 3
    assert len(releases[7].base_releases) == 1
    assert len(releases[8].base_releases) == 2

    # assert list(releases[1].base_releases)[0].release == releases[0].release
    # assert list(releases[2].base_releases)[0].release == releases[1].release
    # assert list(releases[3].base_releases)[0].release == releases[1].release
    # assert list(releases[4].base_releases)[0].release == releases[1].release
    # assert list(releases[4].base_releases)[1].release == releases[3].release
    # assert list(releases[5].base_releases)[0].release == releases[4].release
    # assert list(releases[6].base_releases)[0].release == releases[5].release
    # assert list(releases[6].base_releases)[1].release == releases[1].release
    # assert list(releases[7].base_releases)[0].release == releases[6].release
    # assert list(releases[8].base_releases)[0].release == releases[7].release


def test_time_mine_base_release():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = TimeCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert releases[0].base_releases == None
    assert releases[1].base_releases == [releases[0]]
    assert releases[2].base_releases == [releases[1]]
    assert releases[3].base_releases == [releases[2]]
    assert releases[4].base_releases == [releases[3]]
    assert releases[5].base_releases == [releases[4]]
    assert releases[6].base_releases == [releases[5]]
    assert releases[7].base_releases == [releases[6]]
    assert releases[8].base_releases == [releases[7]]


def test_range_mine_base_release():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = VersionReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = RangeCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert releases[0].base_releases == None
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

