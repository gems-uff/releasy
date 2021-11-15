from typing import List
import pytest

from releasy.project import (Project)
from releasy.release import (Release)

from .mock import VcsMock
from .test_release import (
    reference,
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
        assert "1.0.1" in project.patches
        assert "1.0.2" in project.patches
        assert "2.0.1" in project.patches

    def it_aggregate_patches(project: Project):
        assert "1.0.1" in project.main_releases["1.0.0"].patches
        assert "1.0.2" in project.main_releases["1.0.0"].patches
        assert "2.0.1" in project.main_releases["2.0.0"].patches
        assert project.patches["1.0.1"].main_release.name == "1.0.0"
        assert project.patches["1.0.2"].main_release.name == "1.0.0"
        assert project.patches["2.0.1"].main_release.name == "2.0.0"

    def it_has_pre_releases(project: Project):
        assert len(project.pre_releases) == 2
        assert "2.0.0-alpha1" in project.pre_releases
        assert "2.0.0-beta1" in project.pre_releases

    def it_aggregate_releases(project: Project):
        assert "2.0.0-alpha1" in project.main_releases["2.0.0"].pre_releases
        assert "2.0.0-beta1" in project.main_releases["2.0.0"].pre_releases
        assert project.pre_releases["2.0.0-alpha1"].main_release.name == "2.0.0"
        assert project.pre_releases["2.0.0-beta1"].main_release.name == "2.0.0"

    def it_aggregate_the_release_prefixes(project: Project):
        assert len(project.prefixes) == 2
        assert "v" in project.prefixes
        assert "" in project.prefixes
