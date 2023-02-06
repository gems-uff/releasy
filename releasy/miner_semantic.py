"""Semantic Miner Module

This module categorizes the releases according to their semantic:

- Main release
- Patch releases

This module also categorize releases into pre releases.
"""

from typing import Any, Tuple
from unicodedata import name
from .project import Project
from .release import Release
from .semantic import MainRelease, Patch, SReleaseSet, SemanticRelease
from .miner_base import AbstractMiner


class SemanticReleaseMiner(AbstractMiner):
    """Assign semantic to releases"""
    def __init__(self) -> None:
        super().__init__()
        self.mreleases = SReleaseSet[MainRelease]()
        self.patches = SReleaseSet[Patch]()
        self.r2s = dict[Release, SemanticRelease]()
        self.versions = set[str]()
        self.project = None

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project
        self.releases = project.releases
        self._remove_pre_releases()
        self._mine_semantic_releases()
        self._assign_patches_to_mreleases()
        self._assign_base_releases()
        self._assign_main_base_releases()
        self._assign_prev_semantic_releases()
  
        self.project.main_releases = self.mreleases
        self.project.patches = self.patches
        return (self.project, [])

    def _remove_pre_releases(self):
        #TODO implement pre release logic in the future
        self.releases = [
            release for release in self.releases 
                if not release.version.is_pre_release()
        ]

    def _mine_semantic_releases(self) -> SReleaseSet:
        #TODO implement in ReleaseSet
        for release in sorted(
                self.project.releases.all(), 
                key = lambda r: (r.time, r.version)):

            is_duplicated = release.version.number in self.versions
            if release.version.is_main_release() and not is_duplicated:
                srelease = MainRelease(release)
                self.mreleases.add(srelease)
                self.versions.add(release.version.number)
            else:
                srelease = Patch(release)
                self.patches.add(srelease)  
                srelease.was_main_release = is_duplicated
            self.r2s[release] = srelease
    
    def _assign_patches_to_mreleases(self):
        for patch in self.patches:
            main_release = self._find_patch_main_release(patch)
            if main_release:
                main_release.patches.add(patch)
                patch.main_release = main_release
            else:
                patch.is_orphan = True

    def _find_patch_main_release(self, patch: Patch):
        loop_control = set()
        patch_to_track = [patch]
        while patch_to_track:
            patch = patch_to_track.pop()
            base_srelease = self._get_srelease(patch.release.base_release)
            if isinstance(base_srelease, MainRelease):
                return base_srelease
            elif base_srelease and base_srelease not in loop_control:
                patch_to_track.append(base_srelease)
                loop_control.add(base_srelease)

        return None

    def _assign_base_releases(self):
        for srelease in (self.mreleases | self.patches):
            srelease.base_release = \
                self._get_srelease(srelease.release.base_release)

    def _assign_main_base_releases(self):
        for srelease in (self.mreleases | self.patches):
            main_base_release = srelease.base_release
            if isinstance(main_base_release, Patch):
                main_base_release = main_base_release.main_release
            srelease.main_base_release = main_base_release

    def _assign_prev_semantic_releases(self):
        mreleases = sorted(self.mreleases, 
            key=lambda r: (r.release.version, r.time))
        for i in range(1, len(mreleases)):
            mrelease = mreleases[i]
            prev_mrelease_pos = i-1

            while prev_mrelease_pos >= 0 \
                    and mreleases[prev_mrelease_pos].time > mrelease.time:
                prev_mrelease_pos -= 1
            
            if prev_mrelease_pos >= 0:
                prev_mrelease = mreleases[prev_mrelease_pos]
                mrelease.prev_semantic_release = prev_mrelease

    def _get_srelease(self, release: Release) -> SemanticRelease:
        if release not in self.r2s:
            return None
        return self.r2s[release]

    # def _assign_main_base_release(self):
    #     for mrelease in self.mreleases:
    #         if len(mrelease.base_mreleases) == 1:
    #             mrelease.base_mrelease = mrelease.base_mreleases[0]
    #         elif len(mrelease.base_mreleases) > 1:
    #             releases = sorted(mrelease.base_mreleases.all | set([mrelease])) #FIX version instead of string
    #             mrelease_pos = releases.index(mrelease)
    #             mbase_pos = mrelease_pos - 1
    #             if mbase_pos >= 0:
    #                 mrelease.base_mrelease = releases[mbase_pos]
