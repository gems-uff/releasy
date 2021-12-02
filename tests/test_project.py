from typing import List
import pytest

from releasy.project import Project
from releasy.release import Release
from releasy.semantic import (
    MainRelease,
    Patch,
    PreRelease)

def describe_project():
    @pytest.fixture
    def project():
        project = Project()
        project.add_release(Release('v1.0.0'))
        project.add_release(Release('1.1.0'))
        project.add_release(Release('v1.1.1'))
        project.add_release(Release('v2.0.0beta'))
        return project

    def it_has_release(project: Project):
        assert len(project.releases) == 4

    def it_has_main_releases(project: Project):
        assert set(project.main_releases) \
            == set([MainRelease(Release('v1.0.0')), 
                    MainRelease(Release('1.1.0'))])

    def it_has_patches(project: Project):
        assert set(project.patches) \
            == set([Patch(Release('v1.1.1'))])

    def it_has_pre_releases(project: Project):
        assert set(project.pre_releases) \
            == set([PreRelease(Release('v2.0.0beta'))])

    def it_has_prefixes(project: Project):
        assert project.prefixes == set(['', 'v'])
