from __future__ import annotations
from typing import Set
from .repository import Repository, Tag

class Project:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    @property
    def releases(self) -> Set[Release]:
        return set(self.release)


class Release:
    def __init__(self, project: Project, name: str, tag: Tag) -> None:
        self.project = project
        self.name = name
        self.tag = tag
