from datetime import datetime
import pytest

from releasy.miner import Configuration, DictMiner, GitMiner, Miner
from releasy.release import Release

class DescribeMinerConfiguration:
    def it_has_a_list_plugins(self):
        config = Configuration(
            plugins=[DictMiner({})]
        )
        assert len(config.plugins) == 1
        assert isinstance(config.plugins[0], DictMiner)

class DescribeMiner:
    class WithScenarioA:
        @pytest.fixture
        def scenario(self):
            return [
                {
                    'name': '1.0.0',
                    'timestamp': '2025-01-01',
                    'head': 'a',
                    'author': 'Alice <alice@examplo.com>' 
                },
                {
                    'name': '1.1.0',
                    'timestamp': '2025-01-10',
                    'head': 'b',
                    'author': 'Alice <alice@examplo.com>' 
                },
                {
                    'name': '1.1.1',
                    'timestamp': '2025-01-20',
                    'head': 'c',
                    'author': 'Alice <alice@examplo.com>' 
                }
            ]
            
        def it_create_a_release_graph(self, scenario):
            miner = Miner(Configuration(
                plugins=[DictMiner(scenario)]
            ))
            graph = miner.mine()
            assert len(graph) == 3
        
        def it_use_multiple_plugins(self, scenario):
            r4 = [{
                    'name': '1.1.2',
                    'timestamp': '2025-01-25',
                    'head': 'd',
                    'author': 'Alice <alice@examplo.com>' 
            }] 
            miner = Miner(Configuration(
                plugins=[
                    DictMiner(scenario),
                    DictMiner(r4),
                ]
            ))
            graph = miner.mine()
            assert len(graph) == 4


class DescribeGitMiner:
    def it_mine_releases(self):
        miner = Miner(Configuration(
            plugins=[GitMiner('.')]
        ))
        graph = miner.mine()
        releases = [
            release
            for release in graph.get_all()
            if release.timestamp < datetime(2025, 1, 1, tzinfo=release.timestamp.tzinfo) 
        ]
        assert len(releases) == 25
