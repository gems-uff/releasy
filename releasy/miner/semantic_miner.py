
from typing import Dict
from .factory import AbstractMiner
from ..release_old import (
    ReleaseSet)
from ..project import Project
from ..semantic_old import (
    MainRelease,
    Patch,
    PreRelease,
    SmReleaseSet)


class SemanticMiner(AbstractMiner):
    def mine(self, project: Project, params: Dict[str, object]) -> Project:
        releases = sorted(project.releases)

        for release in releases:
            if release.version.is_main_release():
                main_release = MainRelease(release)
                project.main_releases.add(main_release)
            elif release.version.is_patch():
                patch = Patch(release)
                project.patches.add(patch)
            elif release.version.is_pre_release():
                pre_release = PreRelease(release)
                project.pre_releases.add(pre_release)

        for patch in project.patches:
            main_srelease_version = '.'.join(str(v) for v in patch.version.numbers[0:2] + [0])
            if main_srelease_version in project.main_releases:
                main_srelease = project.main_releases[main_srelease_version]
                main_srelease.add_patch(patch)
            # else: # Sem pai

        for pre_release in project.pre_releases:
            main_srelease_version = '.'.join(str(v) for v in pre_release.version.numbers[0:2] + [0])
            if main_srelease_version in project.main_releases:
                main_srelease = project.main_releases[main_srelease_version]
                main_srelease.add_pre_release(pre_release)

        return project


class OrphanSemanticMiner(AbstractMiner):
    """
    Orphan patches happens when the project creates a patch from a inexistent 
    release. For instance, if there is a patch 1.0.1 but there is no release 
    1.0.0, the patch 1.0.1 is considered orphan.
    """
    
    def mine(self, project: Project, params: Dict[str, object]) -> Project:
        self._fix_orphan_patches(project)
        self._fix_orphan_pre_releases(project)
        return project
    
    def _fix_orphan_patches(self, project: Project) -> None:
        releases = sorted(project.releases)
        orphan_patches = [release.semantic for release in releases
                                    if release.semantic.is_patch() \
                                       and not release.semantic.main_srelease]
        for patch in orphan_patches:
            main_srelease_version = '.'.join(str(v) for v in patch.version.numbers[0:2] + [0])
            if main_srelease_version not in project.main_releases:
                main_release = MainRelease(patch.release)
                project.patches.remove(patch.name)
                project.main_releases.add(main_release)
            else:
                main_release = project.main_releases[main_srelease_version]
                main_release.add_patch(patch)
                project.patches.add(patch)

    def _fix_orphan_pre_releases(self, project: Project) -> None:     
        releases = sorted(project.releases)
        orphan_pre_release = [release.semantic for release in releases
                                    if release.semantic.is_pre_release() \
                                       and not release.semantic.main_srelease]
        for pre_release in orphan_pre_release:
            release_index = releases.index(pre_release.release)
            while release_index < len(releases) \
                    and releases[release_index].semantic.is_pre_release():
                release_index += 1
            main_srelease = releases[release_index].semantic
            main_srelease.add_pre_release(pre_release)
        return project
