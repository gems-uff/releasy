
import releasy
from .mock import DevMock, VcsMockFactory

def test_release_committers():
    strategy = releasy.factory.MiningStrategy.default()
    strategy.vcs_factory = VcsMockFactory()
    factory = releasy.Factory(strategy)
    project = factory.create()
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
    strategy = releasy.factory.MiningStrategy.default()
    strategy.vcs_factory = VcsMockFactory()
    factory = releasy.Factory(strategy)
    project = factory.create()
    assert len(project.releases[0].contributors.authors) == 1
    assert len(project.releases[1].contributors.authors) == 1
    assert len(project.releases[2].contributors.authors) == 1
    assert len(project.releases[3].contributors.authors) == 2
    assert len(project.releases[4].contributors.authors) == 1
    assert len(project.releases[5].contributors.authors) == 1
    assert len(project.releases[6].contributors.authors) == 1
    assert len(project.releases[7].contributors.authors) == 0
    assert len(project.releases[8].contributors.authors) == 1


# def test_release_newcomers():
#     vcs = VcsMock()
#     miner = Miner(vcs=vcs)
#     dev = vcs.dev
#     project = miner.mine_commits()
#     assert len(project.releases[0].newcomers) == 1
#     assert dev.alice in project.releases[0].newcomers

#     assert len(project.releases[1].newcomers) == 1
#     assert dev.bob in project.releases[1].newcomers

#     assert len(project.releases[2].newcomers) == 0
#     assert len(project.releases[3].newcomers) == 1
#     assert dev.charlie in project.releases[3].newcomers

#     assert len(project.releases[4].newcomers) == 0
#     assert len(project.releases[5].newcomers) == 0
#     assert len(project.releases[6].newcomers) == 0
#     assert len(project.releases[7].newcomers) == 0
#     assert len(project.releases[8].newcomers) == 0

