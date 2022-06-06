"""Semantic Miner Module

This module categorizes the releases according to their semantic:

- Main release
- Patch releases

This module also categorize releases into pre releases.
"""

from .release import Project, Release, ReleaseSet
from .semantic import MainRelease, Patch, SReleaseSet, SemanticRelease
from .miner_main import AbstractMiner


class SemanticReleaseMiner(AbstractMiner):
    """Categorize releases into major, minor and main releases"""
    def __init__(self, project: Project) -> None:
        super().__init__(project)
        self.mreleases = SReleaseSet[MainRelease]()
        self.patches = SReleaseSet[Patch]()
        self.r2s = dict[Release, SemanticRelease]()

    def mine(self) -> Project:
        patches = self._mine_patches()
        mreleases = self._mine_mreleases(patches)
        self._assign_patches(mreleases, patches)
        self._assign_commits(mreleases)
        self._assign_commits(patches)

        self.project.main_releases = mreleases
        self.project.patches = patches

        self.mreleases = mreleases
        self.patches = patches

        self._assign_base_releases()
        return self.project

    def _mine_patches(self) -> SReleaseSet:
        patches = SReleaseSet()
        for release in self.project.releases:
            if release.version.is_patch() \
                    and not release.version.is_pre_release():
                patch = Patch(self.project,
                              release.version.number,
                              ReleaseSet([release]))
                self.r2s[release] = patch
                patches.merge(patch)
        return patches

    def _mine_mreleases(self, patches: SReleaseSet) -> SReleaseSet:
        mreleases = SReleaseSet()
        for release in self.project.releases:
            if release.version.is_main_release() \
                    and not release.version.is_pre_release():
                mrelease = MainRelease(self.project, 
                              release.version.number, 
                              ReleaseSet([release]),
                              ReleaseSet())
                self.r2s[release] = mrelease
                mreleases.merge(mrelease)
        return mreleases
    
    def _assign_patches(self, mreleases: SReleaseSet, 
                                     patches: SReleaseSet):
        for patch in patches:
            mversion = '.'.join([str(number) for number in # TODO create a function
                                 patch.releases[0].version.numbers[0:2]] + ['0'])                          
            if mversion in mreleases:
                mreleases[mversion].patches.add(patch)

    def _assign_commits(self, sreleases: SReleaseSet[SemanticRelease]):
        for srelease in sreleases:
            for release in srelease.releases:
                srelease.commits.update(release.commits)

    def _assign_base_releases(self):
        for mrelease in self.mreleases:
            for release in mrelease.releases:
                if release.version.is_main_release():
                    for base_release in release.base_releases:
                        if base_release not in mrelease.releases \
                                and base_release.version.is_main_release():
                            mrelease.base_mreleases.add(self.r2s[base_release])
