"""Semantic Miner Module

This module categorizes the releases according to their semantic:

- Main release
- Patch releases

This module also categorize releases into pre releases.
"""

from typing import Any, Tuple
from unicodedata import name
from .project import Project
from .release import Release, ReleaseSet
from .semantic import MainRelease, Patch, SReleaseSet, SemanticRelease
from .miner_base import AbstractMiner


class SemanticReleaseMiner(AbstractMiner):
    """Categorize releases into major, minor and main releases"""
    def __init__(self) -> None:
        super().__init__()
        self.mreleases = SReleaseSet[MainRelease]()
        self.patches = SReleaseSet[Patch]()
        self.r2s = dict[Release, SemanticRelease]()
        self.mrelease_map = set[str]()

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project
        (mreleases, patches) = self._mine_semantic()

        # self._assign_patches(mreleases, patches)
        # self._assign_commits(mreleases)
        # self._assign_commits(patches)

        self.project.main_releases = mreleases
        self.project.patches = patches

        # self.mreleases = mreleases
        # self.patches = patches

        # self._assign_release()
        # self._assign_base_releases()
        # self._assign_main_base_release()
        return (self.project, [])

    def _mine_semantic(self) -> SReleaseSet:
        mreleases = SReleaseSet[MainRelease]()
        patches = SReleaseSet()
        for release in self.project.releases:
            if not release.version.is_pre_release():
                if release.version.is_patch():
                    patch = Patch(self.project, release)
                    patches.add(patch)
                else:
                    version = '.'.join(
                        [str(number) for number in (release.version.numbers + [0]*(3-len(release.version.numbers)))]
                    )
                    if version not in self.mrelease_map:
                        mrelease = MainRelease(self.project, release)
                        mreleases.add(mrelease)
                        self.mrelease_map.add(version)
                    else:
                        patch = Patch(self.project, release)
                        patches.add(patch)
        return (mreleases, patches)
    
    def _assign_patches(self, mreleases: SReleaseSet[MainRelease], 
                        patches: SReleaseSet[Patch]):
        for patch in patches:
            mversion = '.'.join([str(number) for number in # TODO create a function
                                 patch.releases[0].version.numbers[0:2]] + ['0'])
            if mversion in mreleases:
                mreleases[mversion].patches.add(patch)
                patch.main_release = mreleases[mversion]

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
            for release in mrelease.releases:
                # if release.version.is_main_release():
                for base in release.base_releases:
                    if base not in mrelease.releases:
                        sbase = self.r2s[base]
                        if isinstance(sbase, MainRelease):
                            mbase = sbase
                        elif isinstance(sbase, Patch):
                            mbase = sbase.main_release
                        else: # pre release or orphans
                            mbase = None

                        if mbase and mbase != mrelease:
                            mrelease.base_mreleases.add(mbase)

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
