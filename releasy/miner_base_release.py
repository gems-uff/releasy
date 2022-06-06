"""Base Release Miner

This module mine release base release, that is the release that was created 
before the actual release.
"""
from __future__ import annotations
from releasy.miner_main import AbstractMiner
from releasy.release import Release
from releasy.project import Project

class BaseReleaseMiner(AbstractMiner):
    def mine(self) -> Project:
        commit_to_release = dict[str, Release]()
        for release in self.project.releases:
            if release.head.id not in commit_to_release:
                commit_to_release[release.head.id] = set()
            commit_to_release[release.head.id].add(release)

        for release in self.project.releases:
            for tail in release.tails:
                for parent in tail.parents:
                    if parent.id in commit_to_release:
                        release.base_releases.update(commit_to_release[parent.id])
        return self.project
