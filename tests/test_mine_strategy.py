#import releasy
#import releasy.mine_strategy
import pytest

from releasy.mine_strategy import *

from .miner.vcs.mock import VcsMock


def test_release_matcher():
    release_matcher = ReleaseMatcher()
    with pytest.raises(NotImplementedError):
        release_matcher.is_release(None)


def test_release_sorter():
    release_sorter = ReleaseSorter()
    with pytest.raises(NotImplementedError):
        release_sorter.sort(None)


def test_release_mine_stratety():
    release_strategy = ReleaseMineStratety(None, None, None)
    with pytest.raises(NotImplementedError):
        release_strategy.mine_releases()


def test_commit_mine_strategy():
    commit_strategy = CommitMineStrategy(None, None)
    with pytest.raises(NotImplementedError):
        commit_strategy.mine_commits()


def test_true_release_matcher():
    vcs = VcsMock()
    release_matcher = TrueReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_strategy = TagReleaseMineStrategy(vcs, release_matcher, release_sorter)
    releases = release_strategy.mine_releases()
    assert len(releases) == 9


def test_version_release_matcher():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_strategy = TagReleaseMineStrategy(vcs, release_matcher, release_sorter)
    releases = release_strategy.mine_releases()
    assert len(releases) == 8


def test_time_release_sorter():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_strategy = TagReleaseMineStrategy(vcs, release_matcher, release_sorter)
    releases = release_strategy.mine_releases()
    assert releases[0].name == 'v1.0.0'
    assert releases[1].name == 'v1.0.1'
    assert releases[-1].name == 'v2.1.0'


def test_path_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_strategy = TagReleaseMineStrategy(vcs, release_matcher, release_sorter)
    releases = release_strategy.mine_releases()
    commit_strategy = PathMineStrategy(vcs, releases)
    release_commits = commit_strategy.mine_commits()
    assert len(release_commits['v1.0.0']) == 2
    assert len(release_commits['v1.0.1']) == 2
    assert len(release_commits['v1.1.0']) == 2
    assert len(release_commits['v2.0.0-alpha1']) == 3


def test_time_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_strategy = TagReleaseMineStrategy(vcs, release_matcher, release_sorter)
    releases = release_strategy.mine_releases()
    commit_strategy = TimeMineStrategy(vcs, releases)
    release_commits = commit_strategy.mine_commits()
    assert len(release_commits['v1.0.0']) == 2
    assert len(release_commits['v1.0.1']) == 2
    assert len(release_commits['v1.1.0']) == 3
    assert len(release_commits['v2.0.0-alpha1']) == 2


def test_range_mine_strategy():
    vcs = VcsMock()
    release_matcher = VersionReleaseMatcher()
    release_sorter = TimeReleaseSorter()
    release_strategy = TagReleaseMineStrategy(vcs, release_matcher, release_sorter)
    releases = release_strategy.mine_releases()
    commit_strategy = RangeMineStrategy(vcs, releases)
    release_commits = commit_strategy.mine_commits()
    assert len(release_commits['v1.0.0']) == 2
    assert len(release_commits['v1.0.1']) == 2
    assert len(release_commits['v1.1.0']) == 2
    assert len(release_commits['v2.0.0-alpha1']) == 4