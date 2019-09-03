from releasy.miner.vcs.git import GitVcs
from releasy.miner.vcs.miner import Miner

def test_mine_releases():
    miner = Miner(vcs=GitVcs("."))
    project = miner.mine_releases()
    assert project.releases[0].name == "1.0.0"

def test_mine_commits():
    miner = Miner(vcs=GitVcs("."))
    project = miner.mine_commits()
    assert project.releases[0].tail_commits[0].hashcode == "2e7bc1351f60592d238c76e34ca4e7eda83ed936"
