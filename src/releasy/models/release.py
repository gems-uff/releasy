from typing import List
from datetime import datetime

from releasy.models.commit import Commit, CommitGraph, CommitNode
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