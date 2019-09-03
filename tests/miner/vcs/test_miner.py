from releasy.miner.vcs.miner import Miner

from .mock import VcsMock

def test_mine_project_name():
    miner = Miner(vcs=VcsMock("../../repos/releasy"))
    assert miner._project.name == "releasy"
    miner = Miner(vcs=VcsMock("releasy"))
    assert miner._project.name == "releasy"
    miner = Miner(vcs=VcsMock("./releasy"))
    assert miner._project.name == "releasy"

def test_mine_releases():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_releases()
    assert len(project.releases) == 8
    assert project.releases[0].version == "1.0.0"
    assert project.releases[1].version == "1.0.1"
    assert project.releases[2].version == "1.1.0"
    assert project.releases[3].version == "2.0.0"
    assert project.releases[4].version == "2.0.0"
    assert project.releases[5].version == "2.0.0"
    assert project.releases[6].version == "2.0.1"
    assert project.releases[7].version == "2.1.0"

def test_mine_commits():
    miner = Miner(vcs=VcsMock("releasy"))
    project = miner.mine_commits()
    assert len(project.releases[0].commits) == 2
    assert len(project.releases[1].commits) == 2
    assert len(project.releases[2].commits) == 2
    assert len(project.releases[3].commits) == 3
    assert len(project.releases[4].commits) == 2
    assert len(project.releases[5].commits) == 8
    assert len(project.releases[6].commits) == 0
    assert len(project.releases[7].commits) == 6
    assert len(project.commits) == 20
