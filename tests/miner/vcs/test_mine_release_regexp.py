from datetime import datetime, timedelta
import pytest

from releasy.miner.vcs.miner import Miner
from releasy.exception import MisplacedTimeException

from .mock import DifferentReleaseNameVcsMock


def test_mine_release_regexp():
    miner = Miner(vcs=DifferentReleaseNameVcsMock(), release_prefixes=["v",None])
    project = miner.mine_releases()
    assert len(project.releases) == 7
    assert project.releases[0].version == "0.0.0"
    assert project.releases[1].version == "0.1.0"
    assert project.releases[2].version == "1.0.0"
    assert project.releases[3].version == "1.0.0"
    assert project.releases[4].version == "1.0.0"
    assert project.releases[5].version == "1.0.0"
    assert project.releases[6].version == "1.0.0"

