from typing import List
import pytest

from releasy.project import (Project)
from releasy.release import (Release)

from .mock import VcsMock
from .test_release import (
    release_names,
    release_times,
    releases
)

@pytest.fixture
def project(releases: List[Release]):
    project = Project()
    for release in releases:
        project.add_release(release)
    return project

def describe_project():
    def it_has_release(project: Project):
        assert len(project.releases) == 9

    def it_has_main_release(project: Project):
        assert len(project.main_releases) == 4

    def it_has_patches(project: Project):
        assert len(project.patches) == 3

    def it_has_pre_releases(project: Project):
        assert len(project.pre_releases) == 2

    def it_aggregate_the_release_prefixes(project: Project):
        assert len(project.prefixes) == 2
        assert "v" in project.prefixes
        assert "" in project.prefixes

# def test_suffixes():
#     releases = ReleaseSet()
#     releases.add(Release(ReleaseName("v1.0.0a", "v", "1.0.0", "a"), None, None, None))
#     releases.add(Release(ReleaseName("1.0.1", "", "1.0.1", ""), None, None, None))
#     assert len(releases.suffixes) == 2
