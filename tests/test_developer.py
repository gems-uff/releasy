
import releasy
from releasy.metamodel import Datasource
from .mock import DevMock, VcsMock

def test_release_committers():
    miner = releasy.Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    dev: DevMock = project.datasource.vcs.dev

    assert len(project.releases[0].contributors.committers) == 2
    assert dev.bob in project.releases[0].contributors.committers 
    assert dev.alice in project.releases[0].contributors.committers 

    assert len(project.releases[1].contributors.committers) == 1
    assert dev.bob in project.releases[1].contributors.committers

    assert len(project.releases[2].contributors.committers) == 1
    assert dev.alice in project.releases[2].contributors.committers

    assert len(project.releases[3].contributors.committers) == 3
    assert dev.charlie in project.releases[3].contributors.committers
    assert dev.bob in project.releases[3].contributors.committers
    assert dev.alice in project.releases[3].contributors.committers

    assert len(project.releases[4].contributors.committers) == 2
    assert dev.alice in project.releases[4].contributors.committers
    assert dev.bob in project.releases[4].contributors.committers

    assert len(project.releases[5].contributors.committers) == 1
    assert dev.alice in project.releases[5].contributors.committers 

    assert len(project.releases[6].contributors.committers) == 1
    assert dev.alice in project.releases[6].contributors.committers
    
    assert len(project.releases[7].contributors.committers) == 0

    assert len(project.releases[8].contributors.committers) == 1
    assert dev.alice in project.releases[8].contributors.committers


def test_release_authors():
    miner = releasy.Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    assert len(project.releases[0].contributors.authors) == 1
    assert len(project.releases[1].contributors.authors) == 1
    assert len(project.releases[2].contributors.authors) == 1
    assert len(project.releases[3].contributors.authors) == 2
    assert len(project.releases[4].contributors.authors) == 1
    assert len(project.releases[5].contributors.authors) == 1
    assert len(project.releases[6].contributors.authors) == 1
    assert len(project.releases[7].contributors.authors) == 0
    assert len(project.releases[8].contributors.authors) == 1


def test_release_newcomers():
    miner = releasy.Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    dev: DevMock = project.datasource.vcs.dev
    assert len(project.releases[0].contributors.newcomers) == 2
    assert dev.alice in project.releases[0].contributors.newcomers
    assert dev.bob in project.releases[0].contributors.newcomers

    assert len(project.releases[1].contributors.newcomers) == 0
    assert len(project.releases[2].contributors.newcomers) == 0
    assert len(project.releases[3].contributors.newcomers) == 1
    assert dev.charlie in project.releases[3].contributors.newcomers

    assert len(project.releases[4].contributors.newcomers) == 0
    assert len(project.releases[5].contributors.newcomers) == 0
    assert len(project.releases[6].contributors.newcomers) == 0
    assert len(project.releases[7].contributors.newcomers) == 0
    assert len(project.releases[8].contributors.newcomers) == 0
