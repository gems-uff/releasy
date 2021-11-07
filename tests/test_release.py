from typing import List
import pytest

from releasy.factory import ProjectMiner as Miner
from releasy.metamodel import Datasource
from releasy.release import TYPE_PATCH, ReleaseVersion

from releasy.release import Release
from .mock import VcsMock

@pytest.fixture
def major_release() -> Release:
    return Release("1.0.0")

@pytest.fixture
def release(major_release) -> Release:
    return major_release

@pytest.fixture
def release_with_prefix() -> Release:
    return Release("v1.0.0")

@pytest.fixture
def release_with_suffix() -> Release:
    return Release("1.0.0beta")

def describe_release():
    def it_has_a_name(release: Release):
        assert release.name == "1.0.0"

    def it_has_a_version(release: Release):
        assert release.version.full_name == "1.0.0"


@pytest.fixture
def release_version() -> ReleaseVersion:
    return ReleaseVersion("v1.2.3beta")

@pytest.fixture
def simple_release_version() -> ReleaseVersion:
    return ReleaseVersion("1.2.0")

@pytest.fixture
def unordered_versions():
    return [
        ReleaseVersion("1.2.0"), 
        ReleaseVersion("1.0.0"), 
        ReleaseVersion("1.2.1"), 
        ReleaseVersion("1.3.0"), 
        ReleaseVersion("1.3.0beta"), 
        ReleaseVersion("1.2.2"), 
        ReleaseVersion("2.0.0")
    ]

def describe_release_version():
    def it_has_a_name(release_version: ReleaseVersion):
        assert release_version.full_name == "v1.2.3beta"

    def it_has_a_number(release_version: ReleaseVersion,
                        simple_release_version: ReleaseVersion):
        assert release_version.number == "1.2.3"
        assert simple_release_version.number == "1.2.0"

    def it_may_have_a_prefix(release_version: ReleaseVersion,
                             simple_release_version: ReleaseVersion):
        assert release_version.prefix == "v"
        assert not simple_release_version.prefix

    def it_may_have_a_suffix(release_version: ReleaseVersion,
                             simple_release_version: ReleaseVersion):
        assert release_version.suffix == "beta"
        assert not simple_release_version.suffix

    def it_has_version_numbers(release_version: ReleaseVersion):
        assert release_version.numbers[0] == 1
        assert release_version.numbers[1] == 2
        assert release_version.numbers[2] == 3

    def it_has_order(unordered_versions: List[ReleaseVersion]):
        versions = sorted(unordered_versions)
        assert versions[0].full_name == "1.0.0"
        assert versions[1].full_name == "1.2.0"
        assert versions[2].full_name == "1.2.1"
        assert versions[3].full_name == "1.2.2"
        assert versions[4].full_name == "1.3.0beta"
        assert versions[5].full_name == "1.3.0"
        assert versions[6].full_name == "2.0.0"

    def it_may_be_a_patch(release_version: ReleaseVersion):
        assert release_version.type(TYPE_PATCH)


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
