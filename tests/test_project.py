from typing import List
import pytest

from releasy.project import Project
from releasy.release_old import Release
from releasy.semantic_old import (
    MainRelease,
    Patch,
    PreRelease)

@pytest.fixture
def project():
    project = Project()
    project.releases.add(Release('1.0.0'))
    project.releases.add(Release('1.1.0'))
    project.releases.add(Release('v1.1.1'))
    project.releases.add(Release('1.1.0beta'))
    project.main_releases.add(MainRelease(project.releases['1.0.0']))
    project.main_releases.add(MainRelease(project.releases['1.1.0']))
    project.patches.add(Patch(project.releases['v1.1.1']))
    project.pre_releases.add(PreRelease(project.releases['1.1.0beta']))
    return project

class describe_project():
    def it_has_release(self, project: Project):
        assert len(project.releases) == 4

    def it_has_main_releases(self, project: Project):
        assert set(project.main_releases) \
            == set([MainRelease(Release('1.0.0')), 
                    MainRelease(Release('1.1.0'))])

    def it_has_patches(self, project: Project):
        assert set(project.patches) == set([Patch(Release('v1.1.1'))])

    def it_has_pre_releases(self, project: Project):
         assert set(project.pre_releases) == set([PreRelease(Release('1.1.0beta'))])

    def it_has_prefixes(self, project: Project):
        assert project.prefixes == set(['', 'v'])
