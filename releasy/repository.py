# This module abstract repository objects such as commits and tags
from __future__ import annotations
from typing import Set


class Repository:
    def __init__(self, proxy):
        self.proxy = proxy
        self.proxy.repository = self

    def get_tags(self) -> Set[Tag]:
        tags = self.proxy.get_tags()
        return tags

    def get_commit(self, id: str) -> Commit:
        commit = self.proxy.get_commit(id)
        return commit

    def get_parents(self, commit: Commit) -> Set[Commit]:
        parents = self.proxy.get_parents(commit)
        return parents


class Tag:
    def __init__(self, repository: Repository, name: str, commit: Commit = None, message: str = None) -> None:
        self.repository = repository
        self.name = name
        self.commit = commit
        self._message = message

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Tag):
            return self.name == __o.name
        else:
            return False
        
    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name

    @property
    def message(self):
        if self._message:
            return self._message
        else:
            return self.commit.message


class Commit:
    def __init__(self, repository: Repository, id: str, message: str = None) -> None:
        self.repository = repository
        self.id = id
        self.message = message

    @property
    def parents(self) -> Set[Commit]:
        return self.repository.get_parents(self)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Commit):
            return self.id == __o.id
        else:
            return False
        
    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return self.id[0:8]
