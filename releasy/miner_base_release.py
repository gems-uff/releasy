"""Base Release Miner

This module mine release base release, that is the release that was created 
before the actual release.
"""
from __future__ import annotations
from typing import Any, Tuple
from releasy.miner_base import AbstractMiner
from releasy.release import Commit2ReleaseMapper, Release, ReleaseSet
from releasy.project import Project
from releasy.repository import Commit


class BaseReleaseMiner(AbstractMiner):
    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project

        self.c2r = Commit2ReleaseMapper()
        for arg in args:
            if isinstance(arg, Commit2ReleaseMapper):
                self.c2r = arg
        self._mine_base_releases()

        return self.project, []

    def _mine_base_releases(self) -> None:
        for release in self.project.releases:
            self._mine_release_base_releases(release)
            self._mine_release_main_base_release(release)

    def _mine_release_base_releases(self, release: Release):
        base_releases = ReleaseSet(
            release
            for tail in release.tails 
            for parent in tail.parents 
            for release in self.c2r.get_release(parent))

        base_releases.remove(release)
        release.base_releases = base_releases
    
    def _mine_release_main_base_release(self, release: Release):
        if len(release.base_releases) == 1:
            release.base_release = release.base_releases[0]
        elif len(release.base_releases) > 1:
            #TODO handle v2.0.0, v2.0.1, and 2,0
            releases = [release]
            releases.extend(release.base_releases)
            releases = sorted(releases, key = lambda r: r.version)
            pos = releases.index(release)
            if pos > 0:
                release.base_release = releases[pos-1]
            else:
                release.base_release = releases[1]
