import pytest

from releasy.miner_commit import HistoryCommitMiner
from releasy.miner_release import ReleaseMiner
from releasy.release import Project, ReleaseSet
from releasy.repository import Repository
from releasy.miner_base_release import BaseReleaseMiner
from .mock_repository import MockRepositoryProxy

class describe_base_release_miner():
    @pytest.fixture(autouse=True)
    def init(self) -> ReleaseSet:
        repository = Repository(MockRepositoryProxy())
        project = Project(repository)
        releaseMiner = ReleaseMiner(project)
        project = releaseMiner.mine()
        commitMiner = HistoryCommitMiner(project)
        project = commitMiner.mine()
        base_release_miner = BaseReleaseMiner(project)
        project = base_release_miner.mine()
        self.project = project
        return project

    def it_mine_base_releases(self):
        releases = self.project.release

        assert not releases['0.0.0-alpha1'].base_releases
        assert releases['v0.9.0'].base_releases.names \
            == set(['0.0.0-alpha1'])
        assert releases['v1.0.0'].base_releases.names \
            == set(['v0.9.0'])
        assert releases['v1.0.2'].base_releases.names \
            == set(['v1.0.0'])
        assert releases['1.1.0'].base_releases.names \
            == set(['v0.9.0'])
        assert releases['v2.0.0-alpha1'].base_releases.names \
            == set(['v1.0.0', '1.1.0'])
        assert releases['v2.0.0-beta1'].base_releases.names \
            == set(['v2.0.0-alpha1'])
        assert releases['v2.0.0'].base_releases.names \
            == set(['v1.0.2', 'v0.9.0', 'v2.0.0-beta1'])
        assert releases['v2.0.1'].base_releases \
            == releases['v2.0.0'].base_releases
        assert releases['2.0.0'].base_releases.names \
            == set(['v2.0.0', 'v2.0.1'])
        assert releases['2.1.1pre'].base_releases.names \
            == set(['v2.0.0', 'v2.0.1'])
        assert releases['v2.1.1'].base_releases.names \
            == set(['2.0.0', '2.1.1pre', 'v2.0.0-beta1'])
