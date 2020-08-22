from datetime import datetime, timedelta
import pytest

import releasy
from releasy.miner.vcs.miner import Miner

from .miner.vcs.mock import VcsMock

def test_release_time():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_releases()
    assert project.releases[0].get_time() == datetime(2020, 1, 2,  13, 00)
    assert project.releases[1].get_time() == datetime(2020, 1, 4,  13, 00)
    assert project.releases[2].get_time() == datetime(2020, 1, 7,  12, 00)
    assert project.releases[3].get_time() == datetime(2020, 1, 9,  12, 00)
    assert project.releases[4].get_time() == datetime(2020, 1, 11, 12, 00)
    assert project.releases[5].get_time() == datetime(2020, 1, 14, 13, 00)
    assert project.releases[6].get_time() == datetime(2020, 1, 14, 14, 00)
    assert project.releases[7].get_time() == datetime(2020, 1, 20, 12, 00)


def test_release_base():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_commits()
    assert len(project.releases[0].base_releases) == 0
    assert len(project.releases[1].base_releases) == 1
    assert len(project.releases[2].base_releases) == 1
    assert len(project.releases[3].base_releases) == 2
    assert len(project.releases[4].base_releases) == 1
    assert len(project.releases[5].base_releases) == 1
    assert len(project.releases[6].base_releases) == 1
    assert len(project.releases[7].base_releases) == 1
    assert project.releases[1].base_releases[0] == project.releases[0]
    assert project.releases[2].base_releases[0] == project.releases[0]
    assert project.releases[3].base_releases[0] == project.releases[1]
    assert project.releases[3].base_releases[1] == project.releases[2]
    assert project.releases[4].base_releases[0] == project.releases[3]
    assert project.releases[5].base_releases[0] == project.releases[4]
    assert project.releases[6].base_releases[0] == project.releases[5]
    assert project.releases[7].base_releases[0] == project.releases[5]


def test_release_length():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_commits()
    assert project.releases[0].get_length() == timedelta(days=1)+timedelta(hours=1)
    assert project.releases[1].get_length() == timedelta(days=1)+timedelta(hours=1)
    assert project.releases[2].get_length() == timedelta(days=1)
    assert project.releases[3].get_length() == timedelta(days=4)
    assert project.releases[4].get_length() == timedelta(days=1)
    assert project.releases[5].get_length() == timedelta(days=9)+timedelta(hours=1)
    assert project.releases[6].get_length() == timedelta(days=0)+timedelta(hours=2)
    assert project.releases[7].get_length() == timedelta(days=5)


def ignore_test_pre_releases():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_releases()
    assert len(project.releases[0].pre_releases) == 0
    assert len(project.releases[1].pre_releases) == 0
    assert len(project.releases[2].pre_releases) == 0
    assert len(project.releases[3].pre_releases) == 0
    assert len(project.releases[4].pre_releases) == 0
    assert len(project.releases[5].pre_releases) == 2
    assert len(project.releases[6].pre_releases) == 0
    assert len(project.releases[7].pre_releases) == 0
    assert len(project.get_releases(releasy.RELEASE_TYPE_PRE)) == 2


def ignore_test_duplicated_releases():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_releases()
    assert not project.releases[0].is_duplicated()
    assert not project.releases[1].is_duplicated()
    assert not project.releases[2].is_duplicated()
    assert not project.releases[3].is_duplicated()
    assert not project.releases[4].is_duplicated()
    assert not project.releases[5].is_duplicated()
    assert project.releases[6].is_duplicated()
    assert not project.releases[7].is_duplicated()
    assert project.releases[6].original == project.releases[5]
    assert len(project.get_releases(releasy.RELEASE_TYPE_DUPLICATED)) == 1
    assert len(project.get_releases(releasy.RELEASE_TYPE_COMMON)) == 5
