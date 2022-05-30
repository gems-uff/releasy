from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Set

from releasy.release import Project

from .repository import Repository, Tag


class Miner:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
        self.project = Project()
    
    def mine(self, miner: AbstractMiner) -> Miner:
        mined_project = miner.mine(self.repository, self.project)
        self.project = mined_project
        return miner

    def project(self):
        return self.project


class AbstractMiner(ABC):
    def __init__(self, project: Project) -> None:
        self.project = project

    @abstractmethod
    def mine() -> Project:
        pass

class ReleaseSet():
    def __init__(self, releases = None) -> None:
        self._releases: Dict[str, Release] = {}
        if releases:
            for release in releases:
                self.add(release)

    def __iter__(self):
        return (release for release in self._releases.values())

    def __getitem__(self, key) -> Release:
        if isinstance(key, int):
            release_name = list(self._releases.keys())[key]
            return self._releases[release_name]
        elif isinstance(key, str):
            return self._releases[key]
        else:
            raise TypeError()

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            if item in self._releases:
                return True
        return False

    def add(self, release: Release):
        if release:
            self._releases[release.name] = release

    def update(self, iterable):
        for item in iterable:
            self.add(item)

    def __len__(self):
        return len(self._releases)
