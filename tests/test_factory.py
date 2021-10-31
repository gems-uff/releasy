import releasy

from .mock import VcsMockFactory

def test_factory_wo_param():
    strategy = releasy.factory.MiningStrategy.default()
    strategy.vcs_factory = VcsMockFactory()
    factory = releasy.Factory(strategy)
    factory.create()


def test_factory_w_param():
    strategy = releasy.factory.MiningStrategy.default()
    strategy.vcs_factory = VcsMockFactory()
    factory = releasy.Factory(strategy)
    factory.create(vcs_path = "./")

