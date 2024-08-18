import pytest
from releasy.model import Release, ReleaseType, ReleaseVersion


class DescribeRelease:
    def it_has_name(self, release: Release):
        assert release.name == "1.0.0"

    def it_has_version(self, release: Release):
        assert release.version.number == [1, 0, 0] 
        assert release.version.type == ReleaseType.MAJOR 
        assert release.version.format.name == "Semantic Versioning"

    def it_has_type(self, release: Release):
        assert release.type == ReleaseType.MAJOR
        