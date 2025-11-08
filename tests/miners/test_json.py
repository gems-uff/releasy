import pytest
import json

from releasy.miners.miner import Configuration, Miner
from releasy.miners.json import JsonMiner


class DescribeJsonMiner:
    class WithScenarioA:
        @pytest.fixture
        def scenario(self):
            with open('tests/fixtures/scenario_a.json') as scenario_file:
                scenario = json.load(scenario_file)
                return scenario
            
        def it_mine_releases(self, scenario):
            miner = Miner(Configuration(
                plugins=[JsonMiner(scenario)]
            ))
            project = miner.mine()
            assert len(project.releases) == 3
        
        def it_mine_commits(self, scenario):
            miner = Miner(Configuration(
                plugins=[JsonMiner(scenario)]
            ))
            project = miner.mine()
            assert len(project.commits) == 3

        def it_mine_commit_parents(self, scenario):
            miner = Miner(Configuration(
                plugins=[JsonMiner(scenario)]
            ))
            project = miner.mine()
            commits = project.commits
            assert not commits['a'].parents
            assert commits['b'].parents[0].get().id == 'a'
            assert len(commits['b'].parents) == 1
            assert commits['c'].parents[0].get().id == 'b'
            assert len(commits['c'].parents) == 1
        
        def it_mine_head_commits(self, scenario):
            miner = Miner(Configuration(
                plugins=[JsonMiner(scenario)]
            ))
            project = miner.mine()
            project.releases['1.0.0'].get().head.id == 'a'

        def it_use_multiple_plugins(self, scenario):
            r4 = {
                'releases': [
                    {
                        'name': '1.1.2',
                        'timestamp': '2025-01-25',
                        'head': 'd',
                        'author': 'Alice <alice@examplo.com>' 
                    }
                ],
                'commits': [
                    {
                        'id': 'd',
                        'timestamp': '2025-01-24',
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
