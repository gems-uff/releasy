#import releasy
#import releasy.mine_strategy
import pytest

from releasy.miner import *
from .mock import VcsMock


def test_release_matcher():
    release_matcher = ReleaseMatcher()
    with pytest.raises(NotImplementedError):
        release_matcher.is_release(None)


def test_release_sorter():
    release_sorter = ReleaseSorter()
    with pytest.raises(NotImplementedError):
        release_sorter.sort(None)


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
    assert len(releases) == 9


def test_version_release_matcher():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    assert len(releases) == 8


def test_time_release_sorter():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    assert releases[0].name == 'v1.0.0'
    assert releases[1].name == 'v1.0.1'
    assert releases[-1].name == 'v2.1.0'


def test_path_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = PathCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 2
    assert len(releases[3].commits) == 3


def test_time_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = TimeCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert len(releases['v1.0.0'].commits) == 2
    assert len(releases['v1.0.1'].commits) == 2
    assert len(releases['v1.1.0'].commits) == 3
    assert len(releases['v2.0.0-alpha1'].commits) == 2


def test_range_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_miner = TagReleaseMiner(vcs, release_matcher, release_sorter)
    releases = release_miner.mine_releases()
    commit_miner = RangeCommitMiner(vcs, releases)
    releases = commit_miner.mine_commits()
    assert len(releases[0].commits) == 2
    assert len(releases[1].commits) == 2
    assert len(releases[2].commits) == 2
    assert len(releases[3].commits) == 4
