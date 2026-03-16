import pytest
from datetime import datetime

from releasy.miners.miner import Configuration, Miner
from releasy.miners.git import GitMiner

@pytest.mark.skip
class DescribeGitMiner:
    def it_mine_releases(self):
        miner = Miner(Configuration(
            plugins=[GitMiner('.')]
        ))
        project = miner.mine()
        releases = [
            release_node.get()
            for release_node in project.releases.get_all()
            if release_node.get().timestamp < \
                    datetime(2025, 1, 1, \
                        tzinfo=release_node.get().timestamp.tzinfo) 
        ]
        assert len(releases) == 25

    def it_mine_changes(self):
        pass
    