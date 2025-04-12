from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Iterable, Set

from releasy.commit import Commit, CommitGroup
from releasy.contributor import Contributor
from releasy.version import VersionType, ReleaseVersion


class Release:
    """
    A Release is a group of commits ready to be delivered to its stakeholders
    """
    def __init__(self, 
            version: ReleaseVersion,
            timestamp: datetime,
            head: Commit,
            author: Contributor) -> None:
        self.version = version
        self.timestamp = timestamp
        self.head = head
        self.author = author
        self.commits = CommitGroup()
        self.base_releases = ReleaseSet()
        self.pre_releases = ReleaseSet()

    @property
    def name(self) -> str:
        return self.version.name

    @property
    def type(self) -> VersionType:
        if not self.version:
            return None
            
        return self.version.type

    def set_commits(self, commits: Iterable[Commit]) -> None:
        self.commits = CommitGroup(commits)
    
    def add_base_release(self, release: Release) -> None:
        if not self.base_releases:
            self.base_releases = set()
        self.base_releases.add(release)
    
    def add_pre_release(self, release: Release) -> None:
        if not self.pre_releases:
            self.pre_releases = set()
        self.pre_releases.add(release)


    def __repr__(self) -> str:
        return self.name


class ReleaseSet:
    def __init__(self, releases: Iterable[Release] = None) -> None:
        self._releases = {release.name: release for release in releases} \
                         if releases else {}

    def add(self, release: Release) -> None:
        self._releases[release.name] = release

    def __len__(self) -> int:
        return len(self._releases)

    def __getitem__(self, release_name: str) -> Release:
        if release_name not in self._releases:
            raise KeyError(f"Release {release_name} not found")
        return self._releases[release_name]

    def __iter__(self):
        return iter(self._releases.values())