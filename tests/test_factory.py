import releasy

from .mock import MockStrategy

def test_factory_wo_param():
    factory = releasy.Factory(strategy = MockStrategy())
    factory.create()


def test_factory_w_param():
    factory = releasy.Factory(strategy = MockStrategy())
    factory.create(vcs_path = "./")


