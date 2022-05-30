
import datetime
import pytest

from typing import List
from releasy.commit import Commit
from releasy.project import Project

from releasy.release_old import (
    TYPE_MAIN,
    TYPE_PATCH,
    TYPE_PRE,
    Release, 
    ReleaseSet
)
from releasy.miner.factory import (
    Miner,
    Datasource)
from releasy.miner.collaborator_miner import NewcomerMiner
from releasy.miner.semantic_miner import SemanticMiner
from releasy.semantic_old import (
    DevelopmentPhase,
    MainRelease,
    Patch,
    PreRelease,
    ReleasePhase,
    SmReleaseSet)

from .mock import DevMock, VcsMock, commits

@pytest.fixture
def project() -> Project:
    miner = Miner()
    miner.src(Datasource(vcs=VcsMock()))
    miner.mine_releases()
    miner.mine_commits()
    miner.mine(SemanticMiner())
    miner.mine(NewcomerMiner())
    project = miner.create()
    return project

@pytest.fixture
def main_releases(project: Project) -> List[MainRelease]:
    return project.main_releases

@pytest.fixture
def patches(project: Project) -> ReleaseSet:
    return project.patches

@pytest.fixture
def pre_releases(project: Project) -> SmReleaseSet:
    return project.pre_releases

@pytest.fixture
def dev():
    return DevMock()


class describe_main_release():
    def it_has_a_name(self, main_releases: SmReleaseSet):
        assert main_releases['0.9.0'].name == "0.9.0"
        assert main_releases['1.0.0'].name == "1.0.0"
        assert main_releases['1.1.0'].name == "1.1.0"
        assert main_releases['2.0.0'].name == "2.0.0"

    def it_has_a_fullname(self, main_releases: SmReleaseSet):
        assert main_releases['0.9.0'].fullname == "v0.9.0"
        assert main_releases['1.0.0'].fullname == "v1.0.0"
        assert main_releases['1.1.0'].fullname == "1.1.0"
        assert main_releases['2.0.0'].fullname == "v2.0.0"

    def it_has_a_release(self, main_releases: SmReleaseSet):
        assert len(main_releases) == 4
        assert main_releases['0.9.0'].release.name == "v0.9.0"
        assert main_releases['1.0.0'].release.name == "v1.0.0"
        assert main_releases['1.1.0'].release.name == "1.1.0"
        assert main_releases['2.0.0'].release.name == "v2.0.0"
    
    def it_has_a_version(self, main_releases: SmReleaseSet):
        assert main_releases['0.9.0'].version.number == "0.9.0"
        assert main_releases['1.0.0'].version.number == "1.0.0"
        assert main_releases['1.1.0'].version.number == "1.1.0"
        assert main_releases['2.0.0'].version.number == "2.0.0"

    def it_have_patches(self, main_releases: SmReleaseSet, patches: SmReleaseSet):
        assert not main_releases['0.9.0'].patches
        assert set(main_releases['1.0.0'].patches) \
            == set([patches['1.0.2']])
        assert not main_releases['1.1.0'].patches
        assert set(main_releases['2.0.0'].patches) \
             == set([patches['2.0.1']])

    def it_have_base_main_releases(self, main_releases: SmReleaseSet):
        assert not main_releases['0.9.0'].base_main_releases
        assert main_releases['1.0.0'].base_main_releases \
            == SmReleaseSet([main_releases['0.9.0']])
        assert main_releases['1.1.0'].base_main_releases \
            == SmReleaseSet([main_releases['0.9.0']])
        assert main_releases['2.0.0'].base_main_releases \
            == SmReleaseSet([main_releases['1.0.0'], main_releases['1.1.0']])

    def it_have_base_main_release(self, main_releases: SmReleaseSet):
        assert not main_releases['0.9.0'].base_main_release
        assert main_releases['1.1.0'].base_main_release.name == "0.9.0"
        assert main_releases['2.0.0'].base_main_release.name == "1.1.0"

    def it_has_cycle(self, main_releases: SmReleaseSet):
        assert main_releases['0.9.0'].cycle == datetime.timedelta(hours=1)
        assert main_releases['1.0.0'].cycle == datetime.timedelta(days=2)
        assert main_releases['1.1.0'].cycle == datetime.timedelta(days=4, hours=23)
        assert main_releases['2.0.0'].cycle == datetime.timedelta(days=8, hours=1)

    def it_handle_unordered(self): #TODO
        reference = datetime.datetime(2020, 1, 1, 12, 00)        
        r100 = Release("1.0.0", time=reference)
        r110 = Release("1.1.0", time=reference+datetime.timedelta(days=2))
        r200 = Release("2.0.0", time=reference+datetime.timedelta(days=1))
        r200.add_base_release(r100)
        r110.add_base_release(r100)

    def it_has_commits(self, main_releases: SmReleaseSet):
        assert main_releases['0.9.0'].commits \
            == set([Commit(1)])
        assert main_releases['1.1.0'].commits \
            == set([Commit(6), Commit(5), Commit(2)])
        assert main_releases['2.0.0'].commits \
            == set([Commit(14), Commit(12), Commit(11), Commit(10), Commit(9),
                    Commit(8), Commit(7), Commit(4)])
        
    def it_has_newcomers(self, main_releases: SmReleaseSet, dev: DevMock):
        assert main_releases['0.9.0'].newcomers == set([dev.bob])
        assert not main_releases['1.1.0'].newcomers
        assert main_releases['2.0.0'].newcomers == set([dev.charlie])

    def it_has_development_phase(self, main_releases: SmReleaseSet):
        assert main_releases['1.0.0'].development.start \
            == datetime.datetime(2020, 1, 3, 12, 00)
        assert main_releases['1.0.0'].development.end \
            == datetime.datetime(2020, 1, 4, 13, 00)
        assert main_releases['1.0.0'].development.cycle \
            == datetime.timedelta(days=1, hours=1)

    #TODO evaluate whether the maintenance phase should include the release
    def it_has_maintenance_phase(self, main_releases: SmReleaseSet):
        assert main_releases['1.0.0'].maintenance.start \
            == datetime.datetime(2020, 1, 4, 13, 00)
        assert main_releases['1.0.0'].maintenance.end \
            == datetime.datetime(2020, 1, 14, 12, 00)
        assert main_releases['1.0.0'].maintenance.cycle \
            == datetime.timedelta(days=9, hours=23)

class describe_patch():
    def it_has_a_name(self, patches: SmReleaseSet):
        assert patches['1.0.2'].name == '1.0.2'
        assert patches['2.0.1'].name == '2.0.1'
        assert patches['2.1.1'].name == '2.1.1'

    def it_has_a_release(self, patches: SmReleaseSet):
        assert len(patches) == 3
        assert patches['1.0.2'].release.name == 'v1.0.2'
        assert patches['2.0.1'].release.name == 'v2.0.1'
        assert patches['2.1.1'].release.name == 'v2.1.1'

    def it_has_a_main_release(self, patches: SmReleaseSet):
        assert patches['1.0.2'].main_srelease.name == '1.0.0'
        assert patches['2.0.1'].main_srelease.name == '2.0.0'
        assert not patches['2.1.1'].main_srelease

    def it_has_commits(self, patches: SmReleaseSet):
        assert patches['1.0.2'].commits == patches['1.0.2'].release.commits
        assert patches['2.0.1'].commits == patches['2.0.1'].release.commits
        assert patches['2.1.1'].commits \
            == set([Commit(20), Commit(19), Commit(18), Commit(17), Commit(16),
                    Commit(15)])

    def it_has_newcomers(self, patches: SmReleaseSet):
        assert patches['1.0.2'].newcomers == patches['1.0.2'].release.newcomers
        assert patches['2.0.1'].newcomers == patches['2.0.1'].release.newcomers
        assert not patches['2.1.1'].newcomers

class describe_pre_release():
    def it_has_a_name(self, pre_releases: SmReleaseSet):
        assert pre_releases["2.0.0-alpha1"].name == "2.0.0-alpha1"
        assert pre_releases["2.0.0-beta1"].name == "2.0.0-beta1"

    def it_has_commits(self, pre_releases: SmReleaseSet):
        assert pre_releases["2.0.0-alpha1"].commits \
            == pre_releases["2.0.0-alpha1"].release.commits
        assert pre_releases["2.0.0-beta1"].commits \
            == pre_releases["2.0.0-beta1"].release.commits

    def it_has_newcomers(self, pre_releases: SmReleaseSet):
        assert pre_releases["0.0.0-alpha1"].newcomers \
            == pre_releases["0.0.0-alpha1"].release.newcomers
        assert pre_releases["2.0.0-alpha1"].newcomers \
            == pre_releases["2.0.0-alpha1"].release.newcomers
        assert pre_releases["2.0.0-beta1"].newcomers \
            == pre_releases["2.0.0-beta1"].release.newcomers


@pytest.fixture
def release_phase(main_releases):
    release_phase = DevelopmentPhase(main_releases['1.0.0'])
    return release_phase

class describe_development_phase():

    def it_has_start(self, release_phase):
        assert release_phase.start == datetime.datetime(2020, 1, 3, 12, 00)   

    def it_has_end(self, release_phase):
        assert release_phase.end == datetime.datetime(2020, 1, 4, 13, 00)

    def it_has_cycle(self, release_phase):
        assert release_phase.cycle == datetime.timedelta(days=1, hours=1)