from releasy.miner.vcs.miner import Miner
from .miner.vcs.mock import VcsMock

def test_release_authors():
    vcs = VcsMock()
    miner = Miner(vcs=vcs)
    dev = vcs.dev
    project = miner.mine_commits()
    assert len(project.releases[0].developers.authors) == 1
    assert len(project.releases[1].developers.authors) == 1
    assert len(project.releases[2].developers.authors) == 1
    assert len(project.releases[3].developers.authors) == 3
    assert len(project.releases[4].developers.authors) == 1
    assert len(project.releases[5].developers.authors) == 1
    assert len(project.releases[6].developers.authors) == 0
    assert len(project.releases[7].developers.authors) == 1
    assert project.releases[0].developers.authors[0] == dev.alice
    assert project.releases[1].developers.authors[0] == dev.bob
    assert project.releases[2].developers.authors[0] == dev.alice # fix order
    assert project.releases[3].developers.authors[0] == dev.charlie
    assert project.releases[3].developers.authors[1] == dev.bob
    assert project.releases[3].developers.authors[2] == dev.alice
    assert project.releases[4].developers.authors[0] == dev.alice
    assert project.releases[5].developers.authors[0] == dev.alice
    assert project.releases[7].developers.authors[0] == dev.alice

def test_release_committers():
    vcs = VcsMock()
    miner = Miner(vcs=vcs)
    dev = vcs.dev
    project = miner.mine_commits()
    assert len(project.releases[0].developers.committers) == 1
    assert len(project.releases[1].developers.committers) == 1
    assert len(project.releases[2].developers.committers) == 1
    assert len(project.releases[3].developers.committers) == 3
    assert len(project.releases[4].developers.committers) == 2
    assert len(project.releases[5].developers.committers) == 1
    assert len(project.releases[6].developers.committers) == 0
    assert len(project.releases[7].developers.committers) == 1
    assert project.releases[0].developers.committers[0] == dev.alice
    assert project.releases[1].developers.committers[0] == dev.bob
    assert project.releases[2].developers.committers[0] == dev.alice
    assert project.releases[3].developers.committers[0] == dev.charlie
    assert project.releases[3].developers.committers[1] == dev.bob
    assert project.releases[3].developers.committers[2] == dev.alice
    assert project.releases[4].developers.committers[0] == dev.alice
    assert project.releases[4].developers.committers[1] == dev.bob
    assert project.releases[5].developers.committers[0] == dev.alice
    assert project.releases[7].developers.committers[0] == dev.alice