import pytest
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
        