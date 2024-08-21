from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import re
from typing import Iterable, Set

from releasy.change import Change
from releasy.contributor import Contributor
from releasy.version import VersionType, ReleaseVersion


class Release:
    """
    A Release is a group of changes ready to be delivered to its stakeholders
    """
    def __init__(self, 
            version: ReleaseVersion,
            timestamp: datetime,
            head: Change,
            author: Contributor) -> None:
        self.version = version
        self.timestamp = timestamp
        self.head = head
        self.author = author
        self.changes = set[Change]()
        self.previous: Set[Release] = None

    @property
    def name(self) -> str:
        return self.version.name

    @property
    def type(self) -> VersionType:
        if not self.version:
            return None
            
        return self.version.type

    def add_changes(self, changes: Iterable[Change]) -> None:
        self.changes.update(changes)

    def __repr__(self) -> str:
        return self.name


    