
import datetime
import pytest

from typing import List

from releasy.release import (
    TYPE_MAIN,
    TYPE_PATCH,
    TYPE_PRE,
    Release
)
from releasy.semantic import (
    MainRelease,
    Patch,
    PreRelease
)

from .test_project import project
from .test_release import (
    reference,
    release_names,
    release_times,
    releases
)

@pytest.fixture
def main_releases(releases: List[Release]) -> List[MainRelease]:
    main_releases = [MainRelease(release) for release in releases 
                                          if release.version.type(TYPE_MAIN)]

    patches = [Patch(release) for release in releases 
                              if release.version.type(TYPE_PATCH)
                              and not release.version.type(TYPE_PRE)]
    for main_release in main_releases:
        for patch in patches:
            main_release.add_patch(patch)

    pre_releases = [PreRelease(release) for release in releases 
                                        if release.version.type(TYPE_PRE)]
    for main_release in main_releases:
        for pre_release in pre_releases:
            main_release.add_pre_release(pre_release)

    return main_releases

@pytest.fixture
def patches(main_releases: List[MainRelease]) -> List[Patch]:
    patches = []
    for main_release in main_releases:
        for patch in main_release.patches:
            patches.append(patch)
    return patches

@pytest.fixture
def pre_releases(main_releases: List[MainRelease]) -> List[Patch]:
    pre_releases = []
    for main_release in main_releases:
        for pre_release in main_release.pre_releases:
            pre_releases.append(pre_release)
    return pre_releases

def describe_main_release():
    def it_has_a_name(main_releases: List[MainRelease]):
        assert main_releases[0].name == "1.0.0"
        assert main_releases[1].name == "1.1.0"
        assert main_releases[2].name == "2.0.0"
        assert main_releases[3].name == "2.1.0"

    def it_has_a_release(main_releases: List[MainRelease]):
        assert len(main_releases) == 4
        assert main_releases[0].release.name == "v1.0.0"
        assert main_releases[1].release.name == "1.1.0"
        assert main_releases[2].release.name == "v2.0.0"
        assert main_releases[3].release.name == "v2.1.0"
    
    def it_has_a_version(main_releases: List[MainRelease]):
        assert len(main_releases) == 4
        assert main_releases[0].version.number == "1.0.0"
        assert main_releases[1].version.number == "1.1.0"
        assert main_releases[2].version.number == "2.0.0"
        assert main_releases[3].version.number == "2.1.0"

    def it_have_patches(main_releases: List[MainRelease]):
        assert len(main_releases[0].patches) == 2
        assert "1.0.1" in main_releases[0].patches
        assert "1.0.2" in main_releases[0].patches
        assert len(main_releases[1].patches) == 0
        assert len(main_releases[2].patches) == 1
        assert "2.0.1" in main_releases[2].patches
        assert len(main_releases[3].patches) == 0

    def it_have_base_main_releases(main_releases: List[MainRelease]):
        assert not main_releases[0].base_main_releases
        assert len(main_releases[1].base_main_releases) == 1 
        assert "1.0.0" in main_releases[1].base_main_releases
        assert len(main_releases[2].base_main_releases) == 2
        assert "1.0.0" in main_releases[2].base_main_releases
        assert "1.1.0" in main_releases[2].base_main_releases
        assert len(main_releases[3].base_main_releases) == 1
        assert "2.0.0" in main_releases[3].base_main_releases

    def it_have_a_base_main_release(main_releases: List[MainRelease]):
        assert not main_releases[0].base_main_release
        assert main_releases[1].base_main_release.name == "1.0.0"
        assert main_releases[2].base_main_release.name == "1.1.0"
        assert main_releases[3].base_main_release.name == "2.0.0"

    def it_has_delay(main_releases: List[MainRelease]):
        #assert releases[0].delay == datetime.timedelta(days=2)
        assert main_releases[1].delay == datetime.timedelta(days=5)
        assert main_releases[2].delay == datetime.timedelta(days=8)
        assert main_releases[3].delay == datetime.timedelta(days=6)

    def it_handle_unordered(reference: datetime.datetime):
        r100 = Release("1.0.0", time=reference)
        r110 = Release("1.1.0", time=reference+datetime.timedelta(days=2))
        r200 = Release("2.0.0", time=reference+datetime.timedelta(days=1))
        r200.add_base_release(r100)
        r110.add_base_release(r100)

def describe_patch():
    def it_has_a_name(patches: List[Patch]):
        assert patches[0].name == "1.0.1"
        assert patches[1].name == "1.0.2"
        assert patches[2].name == "2.0.1"

    def it_has_a_release(patches: List[Patch]):
        assert patches[0].release.name == "v1.0.1"
        assert patches[1].release.name == "v1.0.2"
        assert patches[2].release.name == "v2.0.1"

    def it_has_a_main_release(patches: List[Patch]):
        assert patches[0].main_release.name == '1.0.0'
        assert patches[1].main_release.name == '1.0.0'
        assert patches[2].main_release.name == '2.0.0'


def describe_pre_release():
    def it_has_a_name(pre_releases: List[PreRelease]):
        assert pre_releases[0].name == "2.0.0-alpha1"
        assert pre_releases[1].name == "2.0.0-beta1"
