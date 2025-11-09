from __future__ import annotations 

from typing import Iterator, Union
from typing import List
from datetime import datetime

from releasy.models.commit import Commit, CommitGraph, CommitNode, CommitList
from releasy.models.contributor import Contributor
from releasy.models.version import VersionType, ReleaseVersion



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
        self.base_releases = ReleaseList()
        self.commits = CommitList()

    def add_base_release(self, base: 'Release'):
        if base not in self.base_releases:
            self.base_releases.append(base)

    @property
    def name(self) -> str:
        return self.version.name

    @property
    def type(self) -> VersionType:
        if not self.version:
            return None
        return self.version.type

    def __repr__(self) -> str:
        return self.name


class ReleaseList:
    """A list-like collection of releases supporting access by index or name."""
    def __init__(self, releases=None):
        self._releases = [] if releases is None else list(releases)
        self._by_name = {r.name: r for r in self._releases}

    def append(self, release):
        self._releases.append(release)
        self._by_name[release.name] = release

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._releases[key]
        elif isinstance(key, str):
            return self._by_name[key]
        else:
            raise TypeError("ReleaseList indices must be int or str (name)")

    def __iter__(self):
        return iter(self._releases)

    def __len__(self):
        return len(self._releases)

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._by_name
        return item in self._releases

    def names(self):
        return list(self._by_name.keys())
    

class ReleaseNode:
    def __init__(self, release: Release):
        self.release = release
        self.base_releases = list[Release]()
        self.commits = CommitGraph()
        self.tails = list[CommitNode]()

    def get(self) -> Release:
        return self.release


class ReleaseGraph:
    def __init__(self):
        self.nodes = dict[str, ReleaseNode]()
  
    def add(self, release: Release):
        if release.name not in self.nodes:
            release_node = ReleaseNode(release)
            self.nodes[release.name] = release_node
    
    def get(self, reference: str) -> ReleaseNode:
        if reference not in self.nodes:
            return None
        return self.nodes[reference]
    
    def get_all(self) -> List[ReleaseNode]:
        release_nodes = [release_node for release_node in self.nodes.values()]
        return release_nodes

    def __getitem__(self, reference: str | Release):
        if isinstance(reference, Release):
            return self.get(reference.name)
        return self.get(reference)
    
    def __len__(self) -> int:
        return len(self.nodes)