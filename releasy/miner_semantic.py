from functools import reduce
from typing import Dict, Set
import re

from .release import Project
from .semantic import MainRelease
from .miner_main import AbstractMiner, ReleaseSet

class SemanticReleaseMiner(AbstractMiner):
    """
    Mine major, minor and main releases
    """
    def mine(self) -> Project:
        project = self.project

        catalog = {
            'main': {},
            'pre': {},
            'patch': {}
        }

        for release in project.releases:
            mversion = '.'.join([str(number) for number in
                                 release.version.numbers[0:2]] + ['0'])
            
            if mversion not in catalog['main']:
                catalog['main'][mversion] = set()
            if mversion not in catalog['pre']:
                catalog['pre'][mversion] = set()
            if mversion not in catalog['patch']:
                catalog['patch'][mversion] = set()
            
            if release.version.is_pre_release():
                catalog['pre'][mversion].add(release)
            elif release.version.is_patch():
                catalog['patch'][mversion].add(release)
            else:
                catalog['main'][mversion].add(release)


        mreleases: Set[MainRelease] = set()
        for mversion, releases in catalog['main'].items():
            if releases:
                mrelease = MainRelease(project, mversion, releases,
                                       catalog['pre'][mversion],  
                                       catalog['patch'][mversion])
                mreleases.add(mrelease)
            # TODO else orphan

        # TODO project.semantic.main_releases = mrelease
        project.main_releases = ReleaseSet(mreleases)
        return project
