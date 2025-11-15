from __future__ import annotations
from datetime import datetime
from typing import List, Set, Iterator

from releasy.models.contributor import Contributor


class Commit:
    """ 
    A change in a release, such as a commit
    """
    def __init__(
        self,
        id: str,
        message: str = None,
        committer: Contributor = None,
        committer_time: datetime = None,
        parents: CommitList = None,
        author: Contributor =None,
        author_time: datetime =None,
    ) -> None:
        self.id: str = id
        self.message = message
        self.committer = committer
        self.timestamp = committer_time
        self.author = author
        self.author_time = author_time
        self._parents = parents
    
    def __hash__(self) -> int:
        if self.id:
            return hash(self.id)
        else:
            return super.__hash__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Commit):
            return False
        return self.id == other.id
    
    @property
    def parents(self) -> CommitList:
        if self._parents is None:
            raise ValueError(
                "Commit information have not been fetched yet, consider using a "
                "miner to populate it."
            )
        return self._parents

    def set_root(self) -> None:
        self._parents = CommitList()

    def add_parent(self, parent: Commit) -> None:
        if not self._parents:
            self._parents = CommitList()
        self._parents.append(parent)


# deprecated
class CommitNode:
    def __init__(self, commit: Commit):
        self.commit = commit
        self.parents: list[CommitNode] = []
    
    def get(self) -> Commit:
        return self.commit
    
# deprecated
class CommitNode:
    def __init__(self, commit: Commit):
        self.commit = commit
        self.parents: list[CommitNode] = []
    
    def get(self) -> Commit:
        return self.commit
    

class CommitGraph:
    def __init__(self):
        self.commit_nodes: dict[str, CommitNode] = {}

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

class CommitList:
    """A list-like collection of commits supporting access by index or id."""
    def __init__(self, commits: list[Commit] | None = None):
        self._commits: list[Commit] = [] if commits is None else list(commits)
        self._by_id: dict[str, Commit] = {c.id: c for c in self._commits}

    def append(self, commit: Commit) -> None:
        self._commits.append(commit)
        self._by_id[commit.id] = commit

    def __getitem__(self, key: int | str) -> Commit:
        if isinstance(key, int):
            return self._commits[key]
        elif isinstance(key, str):
            return self._by_id[key]
        else:
            raise TypeError("CommitList indices must be int or str (id)")

    def __iter__(self) -> Iterator[Commit]:
        return iter(self._commits)

    def __len__(self) -> int:
        return len(self._commits)

    def __contains__(self, item: str | Commit) -> bool:
        if isinstance(item, str):
            return item in self._by_id
        return item in self._commits

    def ids(self) -> list[str]:
        return list(self._by_id.keys())