from datetime import datetime
import pytest
from releasy.commit import Commit
from releasy.contributor import Contributor
from releasy.version import VersionType, ReleaseVersion
from releasy.release import Release, ReleaseSet


class DescribeRelease:
    def it_has_name(self, scenario_1_releases: ReleaseSet):
        releases = scenario_1_releases
        assert releases["1.0.0"].name == "1.0.0"

    def it_has_version(self, scenario_1_releases: ReleaseSet):
        releases = scenario_1_releases
        assert releases["1.0.0"].version.number == [1, 0, 0]
        assert releases["1.0.0"].version.type == VersionType.MAJOR
        assert releases["1.0.0"].version.format.name == "Semantic Versioning"

    def it_has_type(self, scenario_1_releases: Release):
        releases = scenario_1_releases
        assert releases["1.0.0"].type == VersionType.MAJOR
        assert releases["1.1.0"].type == VersionType.MINOR
        # assert releases["2.0.0-rc.1"].type == VersionType.PRE_RELEASE
        assert releases["2.0.0"].type == VersionType.MAJOR
    
    def it_has_release_timestamp(self, scenario_1_releases: Release):
        releases = scenario_1_releases
        assert releases["1.0.0"].timestamp == datetime(2025, 1, 2)
        assert releases["1.1.0"].timestamp == datetime(2025, 1, 3)
        assert releases["2.0.0-rc.1"].timestamp == datetime(2025, 1, 4)
        assert releases["2.0.0"].timestamp == datetime(2025, 1, 5)
    
    def it_has_author(self, scenario_1_releases: Release):
        releases = scenario_1_releases
        assert releases["1.0.0"].author.name == "Alice"
        assert releases["1.1.0"].author.name == "Alice"
        assert releases["2.0.0-rc.1"].author.name == "Alice"
        assert releases["2.0.0"].author.name == "Alice"

    def it_has_head(self, scenario_1: ReleaseSet):
        releases, commits = scenario_1
        assert releases["1.0.0"].head == commits["1"]
        assert releases["1.1.0"].head == commits["2"]
        assert releases["2.0.0-rc.1"].head == commits["3"]
        assert releases["2.0.0"].head == commits["4"]

    def it_has_base_release(self, scenario_1_releases: ReleaseSet):
        releases = scenario_1_releases
        assert len(releases["1.0.0"].base_releases) == 0
        assert releases["1.0.0"] in releases["1.1.0"].base_releases 
        assert releases["1.1.0"] in releases["2.0.0-rc.1"].base_releases 
        assert releases["1.1.0"] in releases["2.0.0"].base_releases 

    def it_has_pre_release(self, scenario_1_releases: ReleaseSet):
        releases = scenario_1_releases
        assert len(releases["1.0.0"].pre_releases) == 0
        assert len(releases["1.1.0"].pre_releases) == 0
        assert len(releases["2.0.0-rc.1"].pre_releases) == 0
        assert releases["2.0.0-rc.1"] in releases["2.0.0"].pre_releases

    def it_track_changes(self, scenario_1_releases: ReleaseSet):
        releases = scenario_1_releases
        assert len(releases["1.0.0"].commits.all) == 2
        assert len(releases["1.1.0"].commits.all) == 1
        assert len(releases["2.0.0-rc.1"].commits.all) == 1
        assert len(releases["2.0.0"].commits.all) == 1

 