from datetime import datetime, timedelta
import pytest

from releasy.miner import Miner

from .mock import VcsMock

def test_release_time():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_releases()
    assert project.releases[0].time == datetime(2020, 1, 2,  12, 00)
    assert project.releases[1].time == datetime(2020, 1, 3,  12, 00)
    assert project.releases[2].time == datetime(2020, 1, 6,  12, 00)
    assert project.releases[3].time == datetime(2020, 1, 8,  12, 00)
    assert project.releases[4].time == datetime(2020, 1, 10, 12, 00)
    assert project.releases[5].time == datetime(2020, 1, 12, 12, 00)
    assert project.releases[6].time == datetime(2020, 1, 12, 12, 00)


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
    assert project.releases[1].base_releases[0].name == "v1.0.0"
    assert project.releases[2].base_releases[0].name == "v1.0.0"
    assert project.releases[3].base_releases[0].name == "v1.0.1"
    assert project.releases[3].base_releases[1].name == "v1.1.0"
    assert project.releases[4].base_releases[0].name == "v2.0.0-alpha1"
    assert project.releases[5].base_releases[0].name == "v2.0.0-alpha1"
    assert project.releases[5].base_releases[1].name == "v2.0.0-beta1"
    assert project.releases[6].base_releases[0].name == "v2.0.0"


def test_release_length():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_commits()
    # assert project.releases[0].length == timedelta(days=2)
    a = project.releases[1].length
    assert project.releases[1].length == timedelta(days=1)
    assert project.releases[2].length == timedelta(days=3)
    assert project.releases[3].length == timedelta(days=2)
    # assert project.releases[4].length == timedelta(days=2)
    # assert project.releases[5].length == timedelta(days=2)
    # assert project.releases[6].length == timedelta(days=0)
   