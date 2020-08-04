from releasy.miner.vcs.git import GitVcs
from releasy.miner.vcs.miner import Miner

def test_git_mine_releases():
    miner = Miner(vcs=GitVcs("."))
    project = miner.mine_releases()
    assert project.releases[1].name == "1.0.1"

def test_git_mine_commits():
    miner = Miner(vcs=GitVcs("."))
    project = miner.mine_commits()
    assert project.releases[0].tail_commits[0].hashcode == "2e7bc1351f60592d238c76e34ca4e7eda83ed936"

def test_annotated_tags():
    miner = Miner(vcs=GitVcs("."))
    project = miner.mine_releases()
    assert not project.tags[0].is_annotated
    assert project.tags[1].is_annotated