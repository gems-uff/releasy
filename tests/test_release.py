from datetime import datetime
import pytest
from releasy.contributor import Contributor
from releasy.version import VersionType, ReleaseVersion
from releasy.release import Release


class DescribeRelease:
    def it_has_name(self, release: Release):
        assert release.name == "r1.0.0"

    def it_has_version(self, release: Release):
        assert release.version.number == [1, 0, 0] 
        assert release.version.type == VersionType.MAJOR 
        assert release.version.format.name == "Semantic Versioning"

    def it_has_type(self, release: Release):
        assert release.type == VersionType.MAJOR
    
    def it_has_release_timestamp(self, release: Release):
        assert release.timestamp == datetime(2024, 1, 1)
    
    def it_has_author(self, release: Release, alice: Contributor):
        assert release.author == alice
    
    def it_track_changes(self, release: Release):
        pass
        