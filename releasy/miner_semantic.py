from ensurepip import version
from functools import reduce
from typing import Dict, Set

from .release import Project
from .semantic import MainRelease, Patch, SReleaseSet, SemanticRelease
from .miner_main import AbstractMiner
from .collection import ReleaseSet

class SemanticReleaseMiner(AbstractMiner):
    """
    Mine major, minor and main releases
    """
    def mine(self) -> Project:
        patches = self._mine_patches()
        mreleases = self._mine_mreleases(patches)
        self._assign_patches(mreleases, patches)
        self._assign_commits(mreleases)
        self._assign_commits(patches)

        self.project.main_releases = mreleases
        self.project.patches = patches
        return self.project

    def _mine_patches(self) -> SReleaseSet:
        patches = SReleaseSet()
        for release in self.project.releases:
            if release.version.is_patch() \
                    and not release.version.is_pre_release():
                patch = Patch(self.project,
                              release.version.number,
                              ReleaseSet([release]))
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
