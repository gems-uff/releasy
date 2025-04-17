
from __future__ import annotations
from datetime import datetime
from typing import List, Set
from releasy.old.repository_old import Repository


class Commit:
    """ 
    A change in a release, such as a commit
    """
    def __init__(self, id: str, parents: List[Commit] = None, timestamp: datetime = None) -> None:
        self._id = id
        self.timestamp = timestamp
    
    @property
    def id(self) -> str:
        return self._id

    def __hash__(self) -> int:
        if self.id:
            return hash(self.id)
        else:
            return super.__hash__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Commit):
            return False

        return self.id == other.id


class CommitGroup:
    def __init__(self, commits: CommitSet = None):
        self._all = commits

    @property 
    def all(self) -> Set[Commit]:
        return self._all
    
    def add(self, commits: Set[Commit]) -> None:
        for commit in commits:
            self._all.add(commit)
    

class CommitSet:
    def __init__(self, commits: Set[Commit] = None):
        if not commits:
            self._commits = {}
        else:
            self._commits = {commit.id: commit for commit in commits}
    
    def __len__(self) -> int:
        return len(self._commits)

    def add(self, commit: Commit) -> None:
        self._commits[commit.id] = commit
    
    def __getitem__(self, commit_id: str) -> Commit:
        if commit_id not in self._commits:
            return KeyError(f"Commit {commit_id} not found")
        return self._commits[commit_id]


class ChangeAssignmentStrategy:
    pass


class HistoryBasedStrategy(ChangeAssignmentStrategy):
    def assign(releases: Set, repository: Repository):
        return releases
    
