from datetime import datetime, timedelta
import pytest

from releasy.miner_legacy import Miner
from releasy.exception import MisplacedTimeException

from .mock import MisplacedTimeVcsMock

def test_middle_misplaced_time():
    miner = Miner(vcs=MisplacedTimeVcsMock([2]))
    project = miner.mine_commits()
    assert project.releases[0].length == timedelta(days=3)
    assert project.releases[1].length == timedelta(days=3)
    assert project.releases[2].length == timedelta(days=3)

def test_tail_misplaced_time():
    miner = Miner(vcs=MisplacedTimeVcsMock([4]))
    project = miner.mine_commits()
    assert project.releases[0].length == timedelta(days=3)
    #TODO correct implement this test 
    #assert project.releases[1].length == timedelta(days=3)
    assert project.releases[2].length == timedelta(days=3)

def test_head_misplaced_time():
    miner = Miner(vcs=MisplacedTimeVcsMock([7]))
    project = miner.mine_commits()
    # releases are sorted by time, so 1.1.1 comes first
    with pytest.raises(MisplacedTimeException):
         project.releases[0].length
    #TODO release 1 was with 0 commits
    # assert project.releases[1].length == timedelta(days=3)
    assert project.releases[2].length == timedelta(days=3)
