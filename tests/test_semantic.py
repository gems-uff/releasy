
import datetime
import pytest

from typing import List
from releasy.commit import Commit
from releasy.project import Project

from releasy.release import (
    TYPE_MAIN,
    TYPE_PATCH,
    TYPE_PRE,
    Release, 
    ReleaseSet
)
from releasy.miner.factory import (
    Miner, 
    Datasource)
from releasy.semantic import (
    MainRelease,
    Patch,
    PreRelease,
    SmReleaseSet)

from .mock import VcsMock

@pytest.fixture
def project() -> Project:
    miner = Miner()
    miner.src(Datasource(vcs=VcsMock()))
    miner.mine_releases()
    miner.mine_commits()
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

def describe_main_release():
    def it_has_a_name(main_releases: SmReleaseSet):
        assert main_releases['v0.9.0'].name == "v0.9.0"
        assert main_releases['1.1.0'].name == "1.1.0"
        assert main_releases['v2.0.0'].name == "v2.0.0"
        assert main_releases['v2.1.0'].name == "v2.1.0"

    def it_has_a_release(main_releases: SmReleaseSet):
        assert len(main_releases) == 5
        assert main_releases['v0.9.0'].release.name == "v0.9.0"
        assert main_releases['v1.0.0'].release.name == "v1.0.0"
        assert main_releases['1.1.0'].release.name == "1.1.0"
        assert main_releases['v2.0.0'].release.name == "v2.0.0"
        assert main_releases['v2.1.0'].release.name == "v2.1.0"
    
    def it_has_a_version(main_releases: SmReleaseSet):
        assert len(main_releases) == 5
        assert main_releases['v0.9.0'].version.number == "0.9.0"
        assert main_releases['v1.0.0'].version.number == "1.0.0"
        assert main_releases['1.1.0'].version.number == "1.1.0"
        assert main_releases['v2.0.0'].version.number == "2.0.0"
        assert main_releases['v2.1.0'].version.number == "2.1.0"

    def it_have_patches(main_releases: SmReleaseSet, patches: SmReleaseSet):
        assert not main_releases['v0.9.0'].patches
        assert set(main_releases['v1.0.0'].patches) \
            == set([patches['v1.0.2']])
        assert not main_releases['1.1.0'].patches
        assert set(main_releases['v2.0.0'].patches) \
             == set([patches['v2.0.1']])
        assert not main_releases['v2.1.0'].patches

    def it_have_base_main_releases(main_releases: SmReleaseSet):
        assert not main_releases['v0.9.0'].base_main_releases
        assert main_releases['v1.0.0'].base_main_releases \
            == SmReleaseSet([main_releases['v0.9.0']])
        assert main_releases['1.1.0'].base_main_releases \
            == SmReleaseSet([main_releases['v0.9.0']])
        assert main_releases['v2.0.0'].base_main_releases \
            == SmReleaseSet([main_releases['v1.0.0'], main_releases['1.1.0']])
        assert main_releases['v2.1.0'].base_main_releases \
            == SmReleaseSet([main_releases['v2.0.0']])

    def it_have_base_main_release(main_releases: SmReleaseSet):
        assert not main_releases['v0.9.0'].base_main_release
        assert main_releases['1.1.0'].base_main_release.name == "v0.9.0"
        assert main_releases['v2.0.0'].base_main_release.name == "1.1.0"
        assert main_releases['v2.1.0'].base_main_release.name == "v2.0.0"

    def it_has_delay(main_releases: SmReleaseSet):
        #assert main_releases['1.0.0'].delay == datetime.timedelta(days=5) #FIXME
        assert main_releases['1.1.0'].delay == datetime.timedelta(days=4, hours=23)
        assert main_releases['v2.0.0'].delay == datetime.timedelta(days=8, hours=1)
        assert main_releases['v2.1.0'].delay == datetime.timedelta(days=5, hours=23)

    def it_handle_unordered(): #TODO
        reference = datetime.datetime(2020, 1, 1, 12, 00)        
        r100 = Release("1.0.0", time=reference)
        r110 = Release("1.1.0", time=reference+datetime.timedelta(days=2))
        r200 = Release("2.0.0", time=reference+datetime.timedelta(days=1))
        r200.add_base_release(r100)
        r110.add_base_release(r100)

    def it_has_commits(main_releases: SmReleaseSet):
        assert main_releases['v0.9.0'].commits == \
            set([Commit(1), Commit(0)])
        assert main_releases['1.1.0'].commits == \
            set([Commit(6), Commit(5), Commit(2)])
        assert main_releases['v2.0.0'].commits == \
            set([Commit(14), Commit(12), Commit(11), Commit(10), Commit(9),
            Commit(8), Commit(7), Commit(4)])
        assert main_releases['v2.1.0'].commits == \
            set([Commit(20), Commit(19), Commit(18), Commit(17), Commit(16),
                 Commit(15)])
        # assert main_releases['1.1.0'].delay == datetime.timedelta(days=4, hours=23)
        # assert main_releases['v2.0.0'].delay == datetime.timedelta(days=8, hours=1)
        # assert main_releases['v2.1.0'].delay == datetime.timedelta(days=5, hours=23)

def describe_patch():
    def it_has_a_name(patches: SmReleaseSet):
        assert patches['v1.0.2'].name == 'v1.0.2'
        assert patches['v2.0.1'].name == 'v2.0.1'

    def it_has_a_release(patches: SmReleaseSet):
        assert patches['v1.0.2'].release.name == 'v1.0.2'
        assert patches['v2.0.1'].release.name == 'v2.0.1'

    def it_has_a_main_release(patches: SmReleaseSet):
        assert patches['v1.0.2'].main_release.name == 'v1.0.0'
        assert patches['v2.0.1'].main_release.name == 'v2.0.0'

    def it_has_commits(patches: SmReleaseSet):
        assert patches['v1.0.2'].commits == patches['v1.0.2'].release.commits
        assert patches['v2.0.1'].commits == patches['v2.0.1'].release.commits

def describe_pre_release():
    def it_has_a_name(pre_releases: SmReleaseSet):
        assert pre_releases["v2.0.0-alpha1"].name == "v2.0.0-alpha1"
        assert pre_releases["v2.0.0-beta1"].name == "v2.0.0-beta1"

    def it_has_commits(pre_releases: SmReleaseSet):
        assert pre_releases["v2.0.0-alpha1"].commits == \
            pre_releases["v2.0.0-alpha1"].release.commits
        assert pre_releases["v2.0.0-beta1"].commits == \
            pre_releases["v2.0.0-beta1"].release.commits
