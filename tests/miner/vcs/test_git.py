from releasy.miner.vcs.git import GitVcs
from releasy.miner.vcs.miner import Miner

def test_mine_git():
    miner = Miner(vcs=GitVcs("."))
    #project = miner.mine_releases()

