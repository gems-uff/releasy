from __future__ import annotations
from datetime import datetime
from typing import List, Set


class Commit:
    """ 
    A change in a release, such as a commit
    """
    def __init__(self, id: str, timestamp: datetime = None) -> None:
        self.id = id
        self.timestamp = timestamp
    
    def __hash__(self) -> int:
        if self.id:
            return hash(self.id)
        else:
            return super.__hash__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Commit):
            return False

        return self.id == other.id


class CommitNode:
    def __init__(self, commit: Commit):
        self.commit = commit
        self.parents = list[CommitNode]()
    
    def get(self) -> Commit:
        return self.commit
    

class CommitGraph:
    def __init__(self):
        self.commit_nodes = dict[str, CommitNode]()

    def add(self, commit: Commit) -> None:
        if commit.id not in self.commit_nodes:
            commit_node = CommitNode(commit)
            self.commit_nodes[commit.id] = commit_node

    def get(self, reference: str) -> CommitNode:
        if reference not in self.commit_nodes:
            return None
        return self.commit_nodes[reference]
    
    def get_all(self) -> List[CommitNode]:
        commit_nodes = [commit_node for commit_node in self.commit_nodes.values()]
        return commit_nodes

    def __getitem__(self, reference: str | Commit):
        if isinstance(reference, Commit):
            return self.get(reference.id)
        if isinstance(reference, CommitNode):
            return self.get(reference.get().id)
        if isinstance(reference, str):
            return self.get(reference)
        return None
    
    def __len__(self) -> int:
        return len(self.commit_nodes)