import pytest
from releasy.models.project import Project
from releasy.models.release import ReleaseList, Release

class DescribeProject:
    def it_has_a_name(self):
        project = Project("myproject")
        assert project.name == "myproject"

    def it_initializes_with_empty_releases(self):
        project = Project("myproject")
        assert isinstance(project.releases, ReleaseList)
        assert len(project.releases) == 0

    def it_can_add_releases(self, release: Release):
        project = Project("myproject")
        project.releases.append(release)
        assert project.releases[0] == release
        assert len(project.releases) == 1
