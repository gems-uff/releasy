
import releasy
from .mock import VcsMockFactory

def test_release_committers():
    strategy = releasy.factory.MiningStrategy.default()
    strategy.vcs_factory = VcsMockFactory()
    factory = releasy.Factory(strategy)
    project = factory.create()
    assert len(project.releases[0].committers) == 2
    assert len(project.releases[1].committers) == 1
    assert len(project.releases[2].committers) == 1
    assert len(project.releases[3].committers) == 3
    assert len(project.releases[4].committers) == 2
    assert len(project.releases[5].committers) == 1
    assert len(project.releases[6].committers) == 1
    assert len(project.releases[7].committers) == 0
    assert len(project.releases[8].committers) == 1


# def test_release_committers():
#     vcs = VcsMock()
#     miner = Miner(vcs=vcs)
#     dev = vcs.dev
#     project = miner.mine_commits()
#     assert len(project.releases[0].developers.committers) == 2
#     assert len(project.releases[1].developers.committers) == 1
#     assert len(project.releases[2].developers.committers) == 1
#     assert len(project.releases[3].developers.committers) == 3
#     assert len(project.releases[4].developers.committers) == 2
#     assert len(project.releases[5].developers.committers) == 1
#     assert len(project.releases[6].developers.committers) == 3
#     assert len(project.releases[7].developers.committers) == 0
#     assert len(project.releases[8].developers.committers) == 1
#     assert project.releases[0].developers.committers[0] == dev.bob
#     assert project.releases[0].developers.committers[1] == dev.alice
#     assert project.releases[1].developers.committers[0] == dev.bob
#     assert project.releases[2].developers.committers[0] == dev.alice
#     assert project.releases[3].developers.committers[0] == dev.charlie
#     assert project.releases[3].developers.committers[1] == dev.bob
#     assert project.releases[3].developers.committers[2] == dev.alice
#     assert project.releases[4].developers.committers[0] == dev.alice
#     assert project.releases[4].developers.committers[1] == dev.bob
#     assert project.releases[6].developers.committers[0] == dev.alice
#     assert project.releases[6].developers.committers[1] == dev.charlie
#     assert project.releases[6].developers.committers[2] == dev.bob
#     assert project.releases[8].developers.committers[0] == dev.alice


# def test_release_newcomers():
#     vcs = VcsMock()
#     miner = Miner(vcs=vcs)
#     dev = vcs.dev
#     project = miner.mine_commits()
#     assert len(project.releases[0].developers.newcomers) == 1
#     assert len(project.releases[1].developers.newcomers) == 1
#     assert len(project.releases[2].developers.newcomers) == 0
#     assert len(project.releases[3].developers.newcomers) == 1
#     assert len(project.releases[4].developers.newcomers) == 0
#     assert len(project.releases[5].developers.newcomers) == 0
#     assert len(project.releases[6].developers.newcomers) == 1
#     assert len(project.releases[7].developers.newcomers) == 0
#     assert len(project.releases[8].developers.newcomers) == 0
#     assert project.releases[0].developers.newcomers[0] == dev.alice
#     assert project.releases[1].developers.newcomers[0] == dev.bob
#     assert project.releases[3].developers.newcomers[0] == dev.charlie
#     assert project.releases[6].developers.newcomers[0] == dev.charlie
