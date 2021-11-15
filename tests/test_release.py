from typing import List
import pytest
import random
import datetime

from releasy.factory import ProjectMiner as Miner
from releasy.metamodel import Datasource
from releasy.release import TYPE_MAIN, TYPE_MAJOR, TYPE_MINOR, TYPE_PATCH, TYPE_PRE, ReleaseSet, ReleaseVersion

from releasy.release import Release
from .mock import VcsMock


@pytest.fixture
def release_names() -> List[str]:
    return [
        "v1.0.0",
        "v1.0.1",
        "v1.0.2",
        "1.1.0", 
        "v2.0.0-alpha1",
        "v2.0.0-beta1",
        "v2.0.0", 
        "v2.0.1",
        "v2.1.0"
    ]

@pytest.fixture
def reference():
    return datetime.datetime(2020, 1, 1, 12, 00)

@pytest.fixture
def release_times(reference: datetime.datetime) -> List[datetime.datetime]:
    return [
        reference + datetime.timedelta(days=2, hours=1), # "v1.0.0",
        reference + datetime.timedelta(days=4, hours=1), # "v1.0.1",
        reference + datetime.timedelta(days=14, hours=1), # "v1.0.2",
        reference + datetime.timedelta(days=7, hours=1), # "1.1.0", 
        reference + datetime.timedelta(days=9, hours=1), # "v2.0.0-alpha1",
        reference + datetime.timedelta(days=11, hours=1), # "v2.0.0-beta1",
        reference + datetime.timedelta(days=15, hours=1), # "v2.0.0", 
        reference + datetime.timedelta(days=15, hours=2), # "v2.0.1",
        reference + datetime.timedelta(days=21, hours=1), # "v2.1.0"
    ]

@pytest.fixture
def release_versions(release_names: List[str]):
    return [ReleaseVersion(name) for name in release_names]

@pytest.fixture
def releases(release_names: List[str], release_times: List[datetime.datetime]):
    releases = ReleaseSet([Release(name, time=time) for name, time 
                          in zip(release_names, release_times)])

    releases[1].add_base_release(releases[0])
    releases[2].add_base_release(releases[1])
    releases[3].add_base_release(releases[1])
    releases[4].add_base_release(releases[1])
    releases[4].add_base_release(releases[3])
    releases[5].add_base_release(releases[4])
    releases[6].add_base_release(releases[1])
    releases[6].add_base_release(releases[2])
    releases[6].add_base_release(releases[5])
    releases[7].add_base_release(releases[6])
    releases[8].add_base_release(releases[5])
    releases[8].add_base_release(releases[6])
    return releases


def describe_release():
    def it_has_a_name(releases: List[Release]):
        assert releases[0].name == "v1.0.0"
        assert releases[1].name == "v1.0.1"
        assert releases[2].name == "v1.0.2"
        assert releases[3].name == "1.1.0"
        assert releases[4].name == "v2.0.0-alpha1"
        assert releases[5].name == "v2.0.0-beta1"
        assert releases[6].name == "v2.0.0"
        assert releases[7].name == "v2.0.1"
        assert releases[8].name == "v2.1.0"

    def it_has_a_version(releases: List[Release]):
        assert releases[0].version.full_name == "v1.0.0"
        assert releases[1].version.full_name == "v1.0.1"
        assert releases[2].version.full_name == "v1.0.2"
        assert releases[3].version.full_name == "1.1.0"
        assert releases[4].version.full_name == "v2.0.0-alpha1"
        assert releases[5].version.full_name == "v2.0.0-beta1"
        assert releases[6].version.full_name == "v2.0.0"
        assert releases[7].version.full_name == "v2.0.1"
        assert releases[8].version.full_name == "v2.1.0"

    def it_has_base_releases(releases: List[Release]):
        assert not releases[0].base_releases
        assert "v1.0.0" in releases[1].base_releases
        assert "v1.0.1" in releases[2].base_releases
        assert "v1.0.1" in releases[3].base_releases
        assert "1.1.0" in releases[4].base_releases
        assert "v1.0.1" in releases[4].base_releases
        assert "v2.0.0-alpha1" in releases[5].base_releases
        assert "v1.0.1" in releases[6].base_releases
        assert "v1.0.2" in releases[6].base_releases
        assert "v2.0.0-beta1" in releases[6].base_releases
        assert "v2.0.0" in releases[7].base_releases
        assert "v2.0.0-beta1" in releases[8].base_releases
        assert "v2.0.0" in releases[8].base_releases

    def it_has_a_main_base_release(releases: List[Release]):
        assert not releases[0].main_base_release
        assert releases[1].main_base_release.name == "v1.0.0"
        assert releases[2].main_base_release.name == "v1.0.1"
        assert releases[3].main_base_release.name == "v1.0.1"
        assert releases[4].main_base_release.name == "1.1.0"
        assert releases[5].main_base_release.name == "v2.0.0-alpha1"
        assert releases[6].main_base_release.name == "v2.0.0-beta1"
        assert releases[7].main_base_release.name == "v2.0.0"
        assert releases[8].main_base_release.name == "v2.0.0"

    def it_handle_unusual_base_releases() -> Release:
        release = Release("1.0.0")
        release.add_base_release(Release("1.0.1"))
        release.add_base_release(Release("0.9.0"))
        release.add_base_release(Release("0.0.1"))
        assert "0.0.1" in release.base_releases
        assert "0.9.0" in release.base_releases
        assert "1.0.1" in release.base_releases
        assert release.main_base_release.name == "0.9.0"
        
    def it_has_time(releases: List[Release], 
                    release_times: List[datetime.datetime]):
        for release, time in zip(releases, release_times):
            assert release.time == time

    def it_has_delay(releases: List[Release]):
        #TODO: release[0].delay
        assert releases[1].delay == datetime.timedelta(days=2)
        assert releases[2].delay == datetime.timedelta(days=10)
        assert releases[3].delay == datetime.timedelta(days=3)
        assert releases[4].delay == datetime.timedelta(days=2)
        assert releases[5].delay == datetime.timedelta(days=2)
        assert releases[6].delay == datetime.timedelta(days=4)
        assert releases[7].delay == datetime.timedelta(hours=1)
        assert releases[8].delay == datetime.timedelta(days=6)


def describe_release_version():
    def it_has_a_name(release_versions: List[ReleaseVersion]):
        assert release_versions[0].full_name == "v1.0.0"
        assert release_versions[1].full_name == "v1.0.1"
        assert release_versions[2].full_name == "v1.0.2"
        assert release_versions[3].full_name == "1.1.0"
        assert release_versions[4].full_name == "v2.0.0-alpha1"
        assert release_versions[5].full_name == "v2.0.0-beta1"
        assert release_versions[6].full_name == "v2.0.0"
        assert release_versions[7].full_name == "v2.0.1"
        assert release_versions[8].full_name == "v2.1.0"

    def it_has_a_number(release_versions: List[ReleaseVersion]):
        assert release_versions[0].number == "1.0.0"
        assert release_versions[1].number == "1.0.1"
        assert release_versions[2].number == "1.0.2"
        assert release_versions[3].number == "1.1.0"
        assert release_versions[4].number == "2.0.0"
        assert release_versions[5].number == "2.0.0"
        assert release_versions[6].number == "2.0.0"
        assert release_versions[7].number == "2.0.1"
        assert release_versions[8].number == "2.1.0"

    def it_may_have_a_prefix(release_versions: List[ReleaseVersion]):
        assert release_versions[0].prefix == "v"
        assert release_versions[1].prefix == "v"
        assert release_versions[2].prefix == "v"
        assert release_versions[3].prefix == ""
        assert not release_versions[3].prefix
        assert release_versions[4].prefix == "v"
        assert release_versions[5].prefix == "v"
        assert release_versions[6].prefix == "v"
        assert release_versions[7].prefix == "v"
        assert release_versions[8].prefix == "v"

    def it_may_have_a_suffix(release_versions: List[ReleaseVersion]):
        assert not release_versions[0].suffix
        assert release_versions[0].suffix == ""
        assert release_versions[1].suffix == ""
        assert release_versions[2].suffix == ""
        assert release_versions[3].suffix == ""
        assert release_versions[4].suffix == "-alpha1"
        assert release_versions[5].suffix == "-beta1"
        assert release_versions[6].suffix == ""
        assert release_versions[7].suffix == ""
        assert release_versions[8].suffix == ""

    def it_has_version_numbers(release_versions: List[ReleaseVersion]):
        assert release_versions[0].numbers[0] == 1
        assert release_versions[0].numbers[1] == 0
        assert release_versions[0].numbers[2] == 0
        assert release_versions[1].numbers[0] == 1
        assert release_versions[1].numbers[1] == 0
        assert release_versions[1].numbers[2] == 1
        assert release_versions[2].numbers[0] == 1
        assert release_versions[2].numbers[1] == 0
        assert release_versions[2].numbers[2] == 2
        assert release_versions[3].numbers[0] == 1
        assert release_versions[3].numbers[1] == 1
        assert release_versions[3].numbers[2] == 0
        assert release_versions[4].numbers[0] == 2
        assert release_versions[4].numbers[1] == 0
        assert release_versions[4].numbers[2] == 0
        assert release_versions[5].numbers[0] == 2
        assert release_versions[5].numbers[1] == 0
        assert release_versions[5].numbers[2] == 0
        assert release_versions[6].numbers[0]== 2
        assert release_versions[6].numbers[1] == 0
        assert release_versions[6].numbers[2] == 0
        assert release_versions[7].numbers[0] == 2
        assert release_versions[7].numbers[1] == 0
        assert release_versions[7].numbers[2] == 1
        assert release_versions[8].numbers[0] == 2
        assert release_versions[8].numbers[1] == 1
        assert release_versions[8].numbers[2] == 0

    def it_has_order(release_versions: List[ReleaseVersion]):
        shuffled_versions = list(release_versions)
        random.shuffle(shuffled_versions)
        ordered_versions = sorted(shuffled_versions)
        for index in range(len(release_versions)):
            assert ordered_versions[index] == release_versions[index]

    def it_has_type(release_versions: List[ReleaseVersion]):
        assert release_versions[0].type(TYPE_MAJOR)
        assert release_versions[0].type(TYPE_MAIN)
        assert release_versions[1].type(TYPE_PATCH)
        assert not release_versions[1].type(TYPE_MAIN)
        assert release_versions[2].type(TYPE_PATCH)
        assert not release_versions[2].type(TYPE_MAIN)
        assert release_versions[3].type(TYPE_MINOR)
        assert release_versions[3].type(TYPE_MAIN)
        assert release_versions[4].type(TYPE_MAJOR)
        assert release_versions[4].type(TYPE_PRE)
        assert release_versions[5].type(TYPE_MAJOR)
        assert release_versions[5].type(TYPE_PRE)
        assert release_versions[6].type(TYPE_MAJOR)
        assert release_versions[6].type(TYPE_MAIN)
        assert release_versions[7].type(TYPE_PATCH)
        assert not release_versions[7].type(TYPE_MAIN)
        assert release_versions[8].type(TYPE_MINOR)
        assert release_versions[8].type(TYPE_MAIN)


def describe_release_set():
    def it_contains_releases():
        releases = ReleaseSet()
        releases.add(Release("1.0.0"))
        releases.add(Release("1.0.1"))
        assert releases[0].name == "1.0.0"
        assert releases[1].name == "1.0.1"
        assert releases["1.0.0"].name == "1.0.0"
        assert releases["1.0.1"].name == "1.0.1"
        assert len(releases) == 2
