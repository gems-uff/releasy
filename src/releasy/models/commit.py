from __future__ import annotations
from datetime import datetime
from typing import Iterator

from releasy.models.contributor import Contributor
from releasy.models.entity_list import EntityList


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

class CommitList(EntityList[Commit]):
    """A list-like collection of commits supporting access by index or id."""

    def _key(self, item: Commit) -> str:
        return item.id

    def __iter__(self) -> Iterator[Commit]:
        return super().__iter__()

    def ids(self) -> list[str]:
        return self.keys()