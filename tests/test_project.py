
from releasy.project import (Project)
from releasy.release import (Release)

from .mock import VcsMock

def describe_project():
    project = Project()
    major_release = Release("1.0.0")
    minor_release = Release("1.1.0")
    patch = Release("1.1.1")
    project.add_release(major_release)
    project.add_release(minor_release)
    project.add_release(patch)

    def it_has_release():
        assert len(project.releases) == 3
        assert project.releases[0] == major_release
        assert project.releases["1.0.0"] == major_release
        assert project.releases["1.1.0"] == minor_release
        assert project.releases["1.1.1"] == patch

    def it_has_main_release():
        assert len(project.main_releases) == 2
        assert project.main_releases["1.0.0"] == major_release
        assert project.main_releases["1.1.0"] == minor_release

    def it_has_patches():
        assert len(project.patches) == 1
        assert project.patches["1.1.1"] == patch



# def test_prefixes():
#     releases = ReleaseSet()
#     releases.add(Release(ReleaseName("v1.0.0", "v", "1.0.0", ""), None, None, None))
#     releases.add(Release(ReleaseName("1.0.1", "", "1.0.1", ""), None, None, None))
#     assert len(releases.prefixes) == 2


# def test_suffixes():
#     releases = ReleaseSet()
#     releases.add(Release(ReleaseName("v1.0.0a", "v", "1.0.0", "a"), None, None, None))
#     releases.add(Release(ReleaseName("1.0.1", "", "1.0.1", ""), None, None, None))
#     assert len(releases.suffixes) == 2
