
from __future__ import annotations
from datetime import datetime
from typing import List, Set
from releasy.old.repository_old import Repository



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

