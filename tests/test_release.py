
from releasy.factory import ProjectMiner as Miner
from releasy.metamodel import Datasource
from releasy.release import ReleaseVersion

from releasy.release import Release
from .mock import VcsMock

def describe_release():
    def it_has_name():
        release = Release("1.0.0")
        assert release.name == "1.0.0"

    def it_has_version():
        release = Release("1.0.0")
        assert release.version.name == "1.0.0"

    def version_can_be_different_from_name():
        release = Release("v1.0.0")
        assert release.name == "v1.0.0"
        #TODO change to version.number
        #TODO handle prefix / suffix
        #assert release.version.name == "1.0.0"


def test_base_releases():
    miner = Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases
    assert not releases["v1.0.0"].base_releases
    assert len(releases["v1.0.1"].base_releases) == 1
    assert len(releases["v1.0.2"].base_releases) == 1
    assert len(releases["v1.1.0"].base_releases) == 1
    assert len(releases["v2.0.0-alpha1"].base_releases) == 2
    assert len(releases["v2.0.0-beta1"].base_releases) == 1
    assert len(releases["v2.0.0"].base_releases) == 3
    assert len(releases["v2.0.1"].base_releases) == 1
    assert len(releases["v2.1.0"].base_releases) == 2


def test_main_base_release():
    miner = Miner()
    project = miner.mine(Datasource(vcs=VcsMock()))
    releases = project.releases
    assert not releases["v1.0.0"].main_base_release
    assert releases["v1.0.1"].main_base_release == releases["v1.0.0"]
    assert releases["v1.0.2"].main_base_release == releases["v1.0.1"]
    assert releases["v1.1.0"].main_base_release == releases["v1.0.1"]
    assert releases["v2.0.0-alpha1"].main_base_release == releases["v1.1.0"]
    assert releases["v2.0.0-beta1"].main_base_release == releases["v2.0.0-alpha1"]
    assert releases["v2.0.0"].main_base_release == releases["v2.0.0-beta1"]
    assert releases["v2.0.1"].main_base_release == releases["v2.0.0"]
    # assert releases["v2.1.0"].main_base_release == releases["v2.0.0"]
    # TODO FIX ReleaseVersion must handle alfa / beta


def test_release_version():
    version = ReleaseVersion("1.2.3")
    assert version.name == "1.2.3"
    assert version.number[0] == "1"
    assert version.number[1] == "2"
    assert version.number[2] == "3"


def test_release_version_comparator():
    version_a = ReleaseVersion("1.0.0")
    version_b = ReleaseVersion("1.2.3")
    assert version_a < version_b
    assert version_a <= version_b
    assert version_a == version_a
    assert version_b > version_a
    assert version_b >= version_a
    sorted_versions = sorted([version_b, version_a])
    assert sorted_versions[0] == version_a
