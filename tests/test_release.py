from typing import List
import pytest
import random
import datetime
from releasy.commit import Commit

from releasy.miner.factory import ProjectMiner as Miner
from releasy.miner.source import Datasource
from releasy.release import TYPE_MAIN, TYPE_MAJOR, TYPE_MINOR, TYPE_PATCH, TYPE_PRE, ReleaseSet, ReleaseVersion

from releasy.release import Release
from .mock import VcsMock


def describe_release():
    dt_reference = datetime.datetime(2020, 1, 1, 12, 00)
    dt_delay = datetime.timedelta(days=1)

    @pytest.fixture
    def releases():
        releases = ReleaseSet()
        releases.add(Release('v1.0.0', Commit('1', committer_time=dt_reference)))
        releases.add(Release('v1.0.1', time=dt_reference+dt_delay))
        releases.add(Release('v2.0.0'))
        releases['v1.0.1'].add_base_release(releases['v1.0.0'])
        releases['v2.0.0'].add_base_release(releases['v1.0.0'])
        releases['v2.0.0'].add_base_release(releases['v1.0.1'])
        return releases

    def it_has_name(releases: ReleaseSet):
        assert releases[0].name == "v1.0.0"

    def it_has_version(releases: ReleaseSet):
        assert releases['v1.0.0'].version == ReleaseVersion('v1.0.0')

    def it_has_base_releases(releases: ReleaseSet):
        assert releases['v2.0.0'].base_releases \
            == set([releases['v1.0.0'], releases['v1.0.1']])

    def it_has_main_base_release(releases: ReleaseSet):
        assert releases['v2.0.0'].main_base_release == releases['v1.0.1']

    def it_handles_unusual_base_releases(releases: ReleaseSet) -> Release:
        releases['v2.0.0'].add_base_release(Release('v2.0.1'))
        assert releases['v2.0.0'].main_base_release == releases['v1.0.1']
    
    def it_has_time(releases: ReleaseSet):
        assert releases['v1.0.0'].time == dt_reference
        assert releases['v1.0.1'].time == dt_reference+dt_delay

    def it_has_delay(releases: ReleaseSet):
        assert releases['v1.0.1'].delay == dt_delay
    

def describe_release_version():

    @pytest.fixture
    def release_versions() -> List[ReleaseVersion]:
        return [
            ReleaseVersion('v1.0.0'),
            ReleaseVersion('1.0.1'),
            ReleaseVersion('2.0.0beta'),
            ReleaseVersion('2.0.0'),
            ReleaseVersion('2.1.0')]
        
    def it_has_name(release_versions: List[ReleaseVersion]):
        assert release_versions[0].full_name == "v1.0.0"

    def it_has_number(release_versions: List[ReleaseVersion]):
        assert release_versions[0].number == "1.0.0"

    def it_has_prefix(release_versions: List[ReleaseVersion]):
        assert release_versions[0].prefix == "v"
        assert release_versions[1].prefix == ""
        assert release_versions[2].prefix == ""

    def it_has_suffix(release_versions: List[ReleaseVersion]):
        assert release_versions[0].suffix == ""
        assert release_versions[1].suffix == ""
        assert release_versions[2].suffix == "beta"

    def it_has_version_numbers(release_versions: List[ReleaseVersion]):
        assert release_versions[0].numbers == [1, 0, 0]
        assert release_versions[1].numbers == [1, 0, 1]
        assert release_versions[2].numbers == [2, 0, 0]

    def it_has_order(release_versions: List[ReleaseVersion]):
        shuffled_versions = list(release_versions)
        random.shuffle(shuffled_versions)
        ordered_versions:  List[ReleaseVersion] = sorted(shuffled_versions)
        assert ordered_versions[0].full_name == "v1.0.0"
        assert ordered_versions[1].full_name == "1.0.1"
        assert ordered_versions[2].full_name == "2.0.0beta"
        assert ordered_versions[3].full_name == "2.0.0"

    def it_has_type(release_versions: List[ReleaseVersion]):
        assert release_versions[0].type(TYPE_MAJOR)
        assert release_versions[0].type(TYPE_MAIN)
        assert release_versions[1].type(TYPE_PATCH)
        assert release_versions[2].type(TYPE_MAJOR)
        assert release_versions[2].type(TYPE_PRE)
        assert release_versions[3].type(TYPE_MAJOR)
        assert release_versions[3].type(TYPE_MAIN)
        assert release_versions[4].type(TYPE_MINOR)
        assert release_versions[4].type(TYPE_MAIN)

    def it_handle_incomplete_versions():
        v1 = ReleaseVersion("1")
        assert v1.numbers == [1, 0, 0]
        v11 = ReleaseVersion("1.1")
        assert v11.numbers == [1, 1, 0]


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

