
from releasy.miner import Miner

from .mock import VcsMock

def test_mine_project_name():
    miner = Miner("../../repos/releasy")
    assert miner._project.name == "releasy"
    
    miner = Miner("releasy")
    assert miner._project.name == "releasy"

    miner = Miner("./releasy")
    assert miner._project.name == "releasy"

def test_mine_releases():
    vcs = VcsMock()
    miner = Miner("releasy", vcs)
    project = miner.mine_releases()
    assert len(project.releases) == 6
    assert project.releases[0].version == "1.0.0"
    assert project.releases[1].version == "1.0.1"
    assert project.releases[2].version == "1.1.0"
    assert project.releases[3].version == "2.0.0"
    assert project.releases[4].version == "2.0.0"
    assert project.releases[5].version == "2.0.0"

def test_mine_commits():
    vcs = VcsMock()
    miner = Miner("releasy", vcs)
    project = miner.mine_commits()
    assert len(project.releases[0].commits) == 2
    assert len(project.releases[1].commits) == 1
    assert len(project.releases[2].commits) == 2
    assert len(project.releases[3].commits) == 3
    assert len(project.releases[4].commits) == 2
    assert len(project.releases[5].commits) == 1
