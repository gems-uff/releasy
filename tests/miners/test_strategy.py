import json
import pytest

from datetime import datetime
from typing import List

from releasy.miners.miner import Configuration, Miner
from releasy.miners.json import JsonMiner
from releasy.miners.strategy import HistoryBasedStrategy


class DescribeHistoryBasedStrategy:
    class WithScenarioA:
        @pytest.fixture
        def scenario(self):
            with open('tests/fixtures/scenario_a.json') as scenario_file:
                scenario = json.load(scenario_file)
                return scenario
                
        def it_assign_commits_to_releases(self, scenario):
            miner = Miner(Configuration(
                plugins=[
                    JsonMiner(scenario),
                    HistoryBasedStrategy()
                ]
            ))
            project = miner.mine()
            assert project.releases['1.0.0'].commits['a']
            assert project.releases['1.1.0'].commits['b']
            assert project.releases['1.1.1'].commits['c']
        
        def it_assign_base_releases(self, scenario):
            miner = Miner(Configuration(
                plugins=[
                    JsonMiner(scenario),
                    HistoryBasedStrategy()
                ]
            ))
            project = miner.mine()
            assert len(project.releases['1.0.0'].base_releases) == 0
            assert len(project.releases['1.1.0'].base_releases) == 1
            assert project.releases['1.0.0'] in project.releases['1.1.0'].base_releases
            assert len(project.releases['1.1.1'].base_releases) == 1
            assert project.releases['1.1.0'] in project.releases['1.1.1'].base_releases


    class WithScenarioB:
        @pytest.fixture
        def project(self):
            with open('tests/fixtures/scenario_b.json') as scenario_file:
                scenario = json.load(scenario_file)

                miner = Miner(Configuration(
                    plugins=[
                        JsonMiner(scenario),
                        HistoryBasedStrategy()
                    ]
                ))
                project = miner.mine()
                return project
                
        def it_assign_commits_to_releases(self, project):
            releases = project.releases
            assert len(releases['0.0.0-alpha1'].commits) == 1
            assert releases['0.0.0-alpha1'].commits['0']
            
            assert len(releases['v0.9.0'].commits) == 1
            assert releases['v0.9.0'].commits['1']

            assert len(releases['v1.0.0'].commits) == 2 
            assert releases['v1.0.0'].commits['3']
            assert releases['v1.0.0'].commits['2']

            assert len(releases['0.10.1'].commits) == 1
            assert releases['0.10.1'].commits['5']

            assert len(releases['1.1.0'].commits) == 1
            assert releases['1.1.0'].commits['6']

            assert len(releases['1.1.1'].commits) == 2
            assert releases['1.1.1'].commits['7']
            assert releases['1.1.1'].commits['4']

            assert len(releases['v2.0.0-alpha1'].commits) == 1
            assert releases['v2.0.0-alpha1'].commits['8']

            assert len(releases['v2.0.0-beta1'].commits) == 2
            assert releases['v2.0.0-beta1'].commits['10']
            assert releases['v2.0.0-beta1'].commits['9']
            
            assert len(releases['r-1.0.2'].commits) == 1
            assert releases['r-1.0.2'].commits['13']

            assert len(releases['v2.0.0'].commits) == 3
            assert releases['v2.0.0'].commits['14']
            assert releases['v2.0.0'].commits['12']
            assert releases['v2.0.0'].commits['11']

            assert len(releases['v2.0.1'].commits) == 0

            assert len(releases['2.0'].commits) == 1
            assert releases['2.0'].commits['15']
        

        def it_assign_base_releases(self, project):
            releases = project.releases
            assert len(releases['1.1.0'].base_releases) == 2
            assert releases['v1.0.0'] in releases['1.1.0'].base_releases
            assert releases['0.10.1'] in releases['1.1.0'].base_releases


    class WithScenarioC:
        @pytest.fixture
        def project(self):
            with open('tests/fixtures/scenario_c.json') as scenario_file:
                scenario = json.load(scenario_file)

                miner = Miner(Configuration(
                    plugins=[
                        JsonMiner(scenario),
                        HistoryBasedStrategy()
                    ]
                ))
                project = miner.mine()
                return project
        
        def it_assign_commits_to_releases(self, project):
            releases = project.releases
            assert len(releases['1.0.0'].commits) == 3
            assert releases['1.0.0'].commits['3']
            assert releases['1.0.0'].commits['2']
            assert releases['1.0.0'].commits['1']

            assert len(releases['1.0.1'].commits) == 2
            assert releases['1.0.1'].commits['6']
            assert releases['1.0.1'].commits['4']

            assert len(releases['1.1.0'].commits) == 3
            assert releases['1.1.0'].commits['8']
            assert releases['1.1.0'].commits['7']
            assert releases['1.1.0'].commits['5']
        
        def it_assign_base_releases(self, project):
            releases = project.releases
            assert len(releases['1.0.0'].base_releases) == 0
            assert len(releases['1.0.1'].base_releases) == 1
            assert releases['1.0.0'] in releases['1.0.1'].base_releases
            assert len(releases['1.1.0'].base_releases) == 1
            assert releases['1.0.0'] in releases['1.1.0'].base_releases
            
