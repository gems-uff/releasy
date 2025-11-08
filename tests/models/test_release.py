from datetime import datetime
import pytest
from releasy.models.commit import Commit
from releasy.models.contributor import Contributor
from releasy.models.version import VersionType, ReleaseVersion
from releasy.models.release import Release


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
    
    def it_has_author(self, release: Release):
        assert release.author.name == "Alice"

    def it_has_head(self, release: Release, commit: Commit):
        assert release.head == commit

 