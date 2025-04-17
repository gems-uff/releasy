from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Iterable, Set

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