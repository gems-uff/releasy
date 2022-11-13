"""Base Release Miner

This module mine release base release, that is the release that was created 
before the actual release.
"""
from __future__ import annotations
from typing import Any, Tuple
from releasy.miner_base import AbstractMiner
from releasy.release import Release
from releasy.project import Project
from releasy.repository import Commit

class BaseReleaseMiner(AbstractMiner):
    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project
        self.c2r = args[0]
        self._mine_base_releases()
        return (self.project, [])

    def _mine_base_releases(self) -> None:
        for release in self.project.releases:
            for tail in release.tails:
                for parent in tail.parents:
                    if parent in self.c2r:
                        for base_release in self.c2r[parent]:
                            if base_release != release:
                                release.base_releases.add(base_release)
            if not release.tails:
                for base_release in self.c2r[release.head]:
                    if base_release != release:
                            release.base_releases.add(base_release)

        for release in self.project.releases:
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
