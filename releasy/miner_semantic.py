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
        self.sreleases = SReleaseSet[SemanticRelease]()
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
        self._assign_prev_main_releases()
  
        self.project.main_releases = self.mreleases
        self.project.patches = self.patches
        return (self.project, [])

    def _remove_pre_releases(self):
        self.releases = [release for release in 
                                 self.releases 
                                 if not release.version.is_pre_release()]

    def _mine_semantic_releases(self) -> SReleaseSet:
        #TODO implement in ReleaseSet
        for release in sorted(self.project.releases.all(), 
                              key = lambda r: (r.time, r.version)):
            duplicated_release \
                = True if release.version.number in self.versions else False
            if release.version.is_main_release() and not duplicated_release:
                srelease = MainRelease(release)
                self.mreleases.add(srelease)
                self.versions.add(release.version.number)
            else:
                srelease = Patch(release)
                self.patches.add(srelease)  
                if duplicated_release:
                    srelease.was_main_release = True

            self.r2s[release] = srelease
            self.sreleases = SReleaseSet(self.mreleases | self.patches)
    
    def _assign_patches_to_mreleases(self):
        for patch in self.patches:
            main_release = self._track_patch_main_release(patch)
            if main_release:
                main_release.patches.add(patch)
                patch.main_release = main_release
            elif patch.commits:
                patch.is_orphan = True

    def _track_patch_main_release(self, patch: Patch):
        patch_to_track = [patch]
        loop_control = set()
        while patch_to_track:
            patch = patch_to_track.pop()
            if patch.release.base_release:
                sbase_release = self.r2s[patch.release.base_release]
                if isinstance(sbase_release, MainRelease):
                    return sbase_release
                elif sbase_release not in loop_control:
                    loop_control.add(patch)
                    patch_to_track.append(sbase_release)
        return None

    def _assign_base_releases(self):
        for srelease in self.sreleases:
            if srelease.release.base_release:
                srelease.base_release = self.r2s[srelease.release.base_release]
            for base_release in srelease.release.base_releases:
                srelease.base_releases.add(self.r2s[base_release])

    def _assign_main_base_releases(self):
        for srelease in self.sreleases:
            self._assign_release_main_base_release(srelease)
    
    def _assign_release_main_base_release(self, release: SemanticRelease) -> None:
        main_base_releases = SReleaseSet[SemanticRelease]()
        for srelease in release.base_releases:
            if isinstance(srelease, MainRelease):
                main_base_releases.add(srelease)
            else:
                main_base_releases.add(srelease.main_release)
                
        if len(main_base_releases) == 1:
            release.main_base_release = main_base_releases[0]
        elif len(main_base_releases) > 1:
            releases = [release]
            releases.extend(main_base_releases)
            releases = sorted(releases, key = lambda r: r.release.version)
            pos = releases.index(release)
            if pos > 0:
                release.main_base_release = releases[pos-1]
            else:
                release.main_base_release = releases[1]

    def _assign_prev_main_releases(self):        
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
                mrelease.prev_main_release = prev_mrelease

