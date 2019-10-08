from datetime import datetime, timedelta
import pytest

from releasy.miner.vcs.miner import Miner
from releasy.exception import MisplacedTimeException

from .mock import DifferentReleaseNameVcsMock


def test_middle_misplaced_time():
    miner = Miner(vcs=DifferentReleaseNameVcsMock())
    project = miner.mine_releases()
    assert len(project.releases) == 5
    assert project.releases[0].version == "1.0.0"
    assert project.releases[1].version == "1.0.0"
    assert project.releases[2].version == "1.0.0"
    assert project.releases[3].version == "1.0.0"
    assert project.releases[4].version == "1.0.0"

