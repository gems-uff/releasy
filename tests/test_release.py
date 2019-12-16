from datetime import datetime, timedelta
import pytest

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


def test_pre_releases():
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


def test_maintenance_releases():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_releases()
    assert len(project.releases[0].patches) == 1
    assert len(project.releases[1].patches) == 0
    assert len(project.releases[2].patches) == 0
    assert len(project.releases[3].patches) == 0
    assert len(project.releases[4].patches) == 0
    assert len(project.releases[5].patches) == 1
    assert len(project.releases[6].patches) == 0
    assert len(project.releases[7].patches) == 0


def test_linked_releases():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_releases()
    assert project.releases[0].previous_release == None
    assert project.releases[1].previous_release == project.releases[0]
    assert project.releases[2].previous_release == project.releases[1]
    assert project.releases[3].previous_release == project.releases[2]
    assert project.releases[4].previous_release == project.releases[3]
    assert project.releases[5].previous_release == project.releases[4]
    assert project.releases[6].previous_release == project.releases[5]
    assert project.releases[7].previous_release == project.releases[6]
    assert project.releases[0].next_release == project.releases[1]
    assert project.releases[1].next_release == project.releases[2]
    assert project.releases[2].next_release == project.releases[3]
    assert project.releases[3].next_release == project.releases[4]
    assert project.releases[4].next_release == project.releases[5]
    assert project.releases[5].next_release == project.releases[6]
    assert project.releases[6].next_release == project.releases[7]
    assert project.releases[7].next_release == None


def test_linked_feature_releases():
    miner = Miner(vcs=VcsMock())
    project = miner.mine_releases()
    assert project.releases[0].previous_feature_release == None
    assert project.releases[1].previous_feature_release == project.releases[0]
    assert project.releases[2].previous_feature_release == project.releases[0]
    assert project.releases[3].previous_feature_release == project.releases[2]
    assert project.releases[4].previous_feature_release == project.releases[2]
    assert project.releases[5].previous_feature_release == project.releases[2]
    assert project.releases[6].previous_feature_release == project.releases[5]
    assert project.releases[7].previous_feature_release == project.releases[5]
    #TODO implement next_feature_release
    # assert project.releases[0].next_feature_release == project.releases[2]
    # assert project.releases[1].next_feature_release == project.releases[2]
    # assert project.releases[2].next_feature_release == project.releases[5]
    # assert project.releases[3].next_feature_release == project.releases[5]
    # assert project.releases[4].next_feature_release == project.releases[5]
    # assert project.releases[5].next_feature_release == project.releases[7]
    # assert project.releases[6].next_feature_release == project.releases[7]
    # assert project.releases[7].next_feature_release == None