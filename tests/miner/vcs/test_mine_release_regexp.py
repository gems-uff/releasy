from datetime import datetime, timedelta
import pytest

from releasy.miner.vcs.miner import Miner
from releasy.exception import MisplacedTimeException

from .mock import DifferentReleaseNameVcsMock


def test_mine_release_prefixes():
    miner = Miner(vcs=DifferentReleaseNameVcsMock(), release_prefixes=["v",""])
    project = miner.mine_releases()
    assert len(project.releases) == 8
    assert project.releases[0].version == "0.0.0"
    assert project.releases[1].version == "0.1.0"
    assert project.releases[2].version == "1.0.0"
    assert project.releases[3].version == "1.0.0"
    assert project.releases[4].version == "1.0.0"
    assert project.releases[5].version == "1.0.0"
    assert project.releases[6].version == "1.0.0"
    assert project.releases[7].version == "3.0.0"


def test_mine_release_suffixes():
    miner = Miner(vcs=DifferentReleaseNameVcsMock(), release_prefixes=["v",""], ignored_suffixes=["Final"])
    project = miner.mine_releases()
    assert not project.releases[0].suffix
    assert not project.releases[1].suffix
    assert not project.releases[2].suffix
    assert project.releases[3].suffix == "beta1"
    assert project.releases[4].suffix == "beta2"
    assert project.releases[5].suffix == "a1"
    assert project.releases[6].suffix == "b1"
    assert not project.releases[7].suffix
