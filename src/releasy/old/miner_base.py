from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, Set, Tuple

from releasy.old.project import Project

from .repository_old import Repository, Tag


class AbstractMiner(ABC):
    def __init__(self) -> None:
        self.project: Project = None

    @abstractmethod
    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        pass
