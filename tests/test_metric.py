


import pytest

import releasy
from releasy import Metrify
from releasy.metric import Cycle
from releasy.project import Project
from releasy.semantic import MainRelease, SReleaseSet

from tests.mock_repository import MockRepository

@pytest.fixture
def project() -> Project:
    project = releasy.Miner(MockRepository()).apply(
        releasy.FinalReleaseMiner(),
        releasy.HistoryCommitMiner(),
        releasy.BaseReleaseMiner(),
        releasy.SemanticReleaseMiner()
    ).mine()
    return project

@pytest.fixture
def mreleases(project: Project):
    return project.main_releases

class describe_cycle:
    def it_calc(self, mreleases: SReleaseSet[MainRelease]):
        pass
        