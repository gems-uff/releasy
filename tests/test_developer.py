from releasy.miner.vcs.miner import Miner
from .miner.vcs.mock import VcsMock

def test_release_authors():
    vcs = VcsMock()
    miner = Miner(vcs=vcs)
    dev = vcs.dev
    project = miner.mine_commits()
    len(project.releases[0].developers.authors) == 1
    len(project.releases[3].developers.authors) == 2
    