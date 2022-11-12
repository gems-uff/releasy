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
    """Categorize releases into major, minor and patch"""
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
  
        self.project.main_releases = self.mreleases
        self.project.patches = self.patches

        # self.mreleases = mreleases
        # self.patches = patches

        # self._assign_release()
        # self._assign_base_releases()
        # self._assign_main_base_release()
        return (self.project, [])

    def _remove_pre_releases(self):
        self.releases = [release for release in 
                                 self.releases 
                                 if not release.version.is_pre_release()]

    def _mine_semantic_releases(self) -> SReleaseSet:
        #TODO implement in ReleaseSet
        for release in sorted(self.project.releases.all(), 
                              key = lambda r: (r.time, r.version)):
            if ((release.version.is_main_release() 
                        and release.version.number not in self.versions)
                    or not release.base_releases):
                srelease = MainRelease(release)
                self.mreleases.add(srelease) 
                self.versions.add(release.version.number)
            else:
                srelease = Patch(release)
                self.patches.add(srelease)  
            self.r2s[release] = srelease
    
    def _assign_patches_to_mreleases(self):
        for patch in self.patches:
            main_release = self._track_patch_main_release(patch)
            main_release.patches.add(patch)
            patch.main_release = main_release

    def _track_patch_main_release(self, patch: Patch):
        patch_to_track = [patch]
        while patch_to_track:
            patch = patch_to_track.pop()
            sbase_release = self.r2s[patch.release.base_release]
            if isinstance(sbase_release, MainRelease):
                return sbase_release
            else:
                patch_to_track.append(sbase_release)

    def _assign_release(self):
        sreleases: SReleaseSet[SemanticRelease] = self.mreleases | self.patches
        for srelease in sreleases:
            srelease.release = srelease.releases.first(lambda r: r.time)

    def _assign_commits(self, sreleases: SReleaseSet[SemanticRelease]):
        for srelease in sreleases:
            for release in srelease.releases:
                srelease.commits.update(release.commits)

    def _assign_base_releases(self):
        for mrelease in self.mreleases:
            if mrelease.release.base_release:
                mrelease.base_release = self.r2s[mrelease.release.base_release]
        for patch in self.patches:
            if patch.release.base_release:
                patch.base_release = self.r2s[patch.release.base_release]

    def _assign_main_base_release(self):
        for mrelease in self.mreleases:
            if len(mrelease.base_mreleases) == 1:
                mrelease.base_mrelease = mrelease.base_mreleases[0]
            elif len(mrelease.base_mreleases) > 1:
                releases = sorted(mrelease.base_mreleases.all | set([mrelease])) #FIX version instead of string
                mrelease_pos = releases.index(mrelease)
                mbase_pos = mrelease_pos - 1
                if mbase_pos >= 0:
                    mrelease.base_mrelease = releases[mbase_pos]
