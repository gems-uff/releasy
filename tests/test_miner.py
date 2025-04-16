import pytest
import json

from datetime import datetime

from releasy.miner import Configuration, JsonMiner, GitMiner, Miner
from releasy.release import Release

class DescribeMinerConfiguration:
    def it_has_a_list_plugins(self):
        config = Configuration(
            plugins=[JsonMiner({})]
        )
        assert len(config.plugins) == 1
        assert isinstance(config.plugins[0], JsonMiner)

class DescribeJsonReleaseMiner:
    class WithScenarioA:
        @pytest.fixture
        def scenario(self):
            with open('tests/fixtures/scenario_a.json') as scenario_file:
                scenario = json.load(scenario_file)
                return scenario
            
        def it_create_a_release_graph(self, scenario):
            miner = Miner(Configuration(
                plugins=[JsonMiner(scenario)]
            ))
            project = miner.mine()
            assert len(project.releases) == 3
        
        def it_use_multiple_plugins(self, scenario):
            r4 = {
                'releases': [
                    {
                        'name': '1.1.2',
                        'timestamp': '2025-01-25',
                        'head': 'd',
                        'author': 'Alice <alice@examplo.com>' 
                    }
                ]
            } 
            miner = Miner(Configuration(
                plugins=[
                    JsonMiner(scenario),
                    JsonMiner(r4),
                ]
            ))
            project = miner.mine()
            assert len(project.releases) == 4


class DescribeGitReleaseMiner:
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
