from __future__ import annotations
from abc import ABC, abstractmethod
import re
from typing import Set

from releasy.version import VersionType, ReleaseVersion


class Release:
    """
    A Release is a group of changes ready to be delivered to its stakeholders
    """
    def __init__(self, version: ReleaseVersion) -> None:
        self.version = version
        self.previous: Set[Release] = None

    @property
    def name(self) -> str:
        return self.version.name

    @property
    def type(self) -> VersionType:
        if not self.version:
            return None
            
        return self.version.type

    
    @property
    def commits(self) -> Set[Change]:
        pass 

    def __repr__(self) -> str:
        return self.name



class Change:
    pass


