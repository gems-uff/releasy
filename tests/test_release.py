from datetime import datetime, timedelta
import pytest

from releasy.miner.miner import Miner

from .mock import VcsMock

def test_release_time():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_releases()
    assert project.releases[0].time == datetime(2020, 1, 2,  12, 00)
    assert project.releases[1].time == datetime(2020, 1, 4,  12, 00)
    assert project.releases[2].time == datetime(2020, 1, 7,  12, 00)
    assert project.releases[3].time == datetime(2020, 1, 9,  12, 00)
    assert project.releases[4].time == datetime(2020, 1, 11, 12, 00)
    assert project.releases[5].time == datetime(2020, 1, 14, 12, 00)
    assert project.releases[6].time == datetime(2020, 1, 14, 12, 00)


def test_release_base():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_commits()
    assert len(project.releases[0].base_releases) == 0
    assert len(project.releases[1].base_releases) == 1
    assert len(project.releases[2].base_releases) == 1
    assert len(project.releases[3].base_releases) == 2
    assert len(project.releases[4].base_releases) == 1
    assert len(project.releases[5].base_releases) == 2
    assert len(project.releases[6].base_releases) == 1
    assert project.releases[1].base_releases[0] == project.releases[0]
    assert project.releases[2].base_releases[0] == project.releases[1]
    assert project.releases[3].base_releases[0] == project.releases[1]
    assert project.releases[3].base_releases[1] == project.releases[2]
    assert project.releases[4].base_releases[0] == project.releases[3]
    assert project.releases[5].base_releases[0] == project.releases[1]
    assert project.releases[5].base_releases[1] == project.releases[4]
    assert project.releases[6].base_releases[0] == project.releases[5]


def test_release_length():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_commits()
    assert project.releases[0].length == timedelta(days=1)
    assert project.releases[1].length == timedelta(days=1)
    assert project.releases[2].length == timedelta(days=1)
    assert project.releases[3].length == timedelta(days=4)
    assert project.releases[4].length == timedelta(days=1)
    assert project.releases[5].length == timedelta(days=9)
    assert project.releases[6].length == timedelta(days=0)
