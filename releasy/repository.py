# This module abstract repository objects such as commits and tags
from __future__ import annotations
from abc import ABC, abstractclassmethod
from collections import OrderedDict
from mimetypes import init
from typing import Callable, Dict, Iterator, Set
from datetime import datetime


class Repository:
    """ 
    A repository stores Tags and Commits
    """
    def __init__(self, proxy: RepositoryProxy):
        proxy.repository = self # TODO better alternative
        self.name: str = proxy.name
        self.proxy = proxy
        self.commit_cache = CommitCache(proxy)

    def get_tags(self) -> Set[Tag]:
        tags = self.proxy.fetch_tags()
        return tags

    def get_commit(self, id: str) -> Commit:
        commit = self.commit_cache.fetch_commit(id)
        return commit

    def get_parents(self, commit: Commit) -> CommitSet:
        parents = self.proxy.fetch_commit_parents(commit)
        return parents

    def diff(self, commit_a: Commit, commit_b: Commit, parse_files: bool) -> DiffDelta:
        diff_delta = self.proxy.diff(commit_a, commit_b, parse_files)
        return diff_delta


class CommitCache:
    """
    Implement cache to improve fech commit performance
    """
    def __init__(self, proxy: RepositoryProxy) -> None:
        self.cache: Dict[str, Commit] = {}
        self.proxy = proxy

    def fetch_commit(self, commit_id: str) -> Commit:
        if commit_id not in self.cache:
            commit = self.proxy.fetch_commit(commit_id)
            self.cache[commit_id] = commit
        return self.cache[commit_id]


class RepositoryProxy(ABC):
    """ 
    An adapter to enable developers creating specific repository, such as Git 
    """
    def __init__(self) -> None:
        super().__init__()
        self.repository: Repository = None #TODO better alternative
        self.name: str = None

    @abstractclassmethod
    def fetch_tags(self) -> Set[Tag]:
        pass

    @abstractclassmethod
    def fetch_commit(self, id: str) -> Commit:
        pass

    @abstractclassmethod
    def fetch_commit_parents(self, commit: Commit) -> CommitSet:
        pass

    @abstractclassmethod
    def diff(self, commit_a: Commit, commit_b: Commit, parse_files:bool) -> DiffDelta:
        pass


class Tag:
    """
    A Tag represents a reference to a commit, which is a potential release
    """
    def __init__(self, repository: Repository, name: str, commit: Commit = None,
                 message: str = None, author: str = None, time: datetime = None) -> None:
        self.repository = repository
        self.name = name
        self.commit = commit
        self.author = author
        if message:
            self.message = message
        else:
            self.message = ""
        if time:
            self.time = time
        elif commit:
            self.time = commit.committer_time
        if message or time:
            self.is_annotated = True
        else:
            self.is_annotated = False

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Tag):
            return self.repository == __o.repository and self.name == __o.name
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.repository, self.name))

    def __repr__(self) -> str:
        return self.name


class Commit:
    """
    A Commit represents a change
    """
    def __init__(self, repository: Repository, id: str, message: str = None, 
                 committer: str = None, committer_time: datetime = None,
                 author: str = None, author_time: datetime = None) -> None:
        self.repository = repository
        self.id = id
        self.message = message
        self._parents = None # Lazy loaded
        self.committer = committer
        self.committer_time = committer_time
        self.author = author
        self.author_time = author_time

    @property
    def parents(self) -> CommitSet:
        if not self._parents:
            self._parents = self.repository.get_parents(self)
        return self._parents

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Commit):
            return self.repository == __o.repository and self.id == __o.id
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((self.repository, self.id))

    def __repr__(self) -> str:
        return self.id[0:8]

    def diff(self, commit: Commit, parse_files:bool = False) -> DiffDelta:
        delta = self.repository.diff(self, commit, parse_files)
        return delta
    
    # TODO commit.history_until(release_commits)
    # for commit in commits:
    #     release_commits = commit.history_until(release_commits)


class DiffDelta:
    def __init__(self, insertions: int, deletions: int, files_changed: int, 
            files: Set[str]):
        self.insertions = insertions
        self.deletions = deletions
        self.files_changed = files_changed
        self.files = files
   
    @property
    def churn(self) -> int:
        return self.insertions + self.deletions


class CommitSet:
    def __init__(self, commits: Set[Commit] = None) -> None:
        self._commits = OrderedDict[str, Commit]()
        if commits:
            self.update(commits)
    
    def __contains__(self, item) -> bool:
        if isinstance(item, str) and item in self._commits:
            return True
        elif isinstance(item, Commit) and item.id in self._commits:
            return True
        return False

    def __getitem__(self, key) -> Commit:
        if isinstance(key, int):
            commit_id = list(self._commits.keys())[key]
            return self._commits[commit_id]
        elif isinstance(key, str):
            return self._commits[key]
        else:
            raise TypeError()

    def __iter__(self) -> Iterator[Commit]:
        return iter(self._commits.values())

    def __eq__(self, __o: object) -> bool:
        return self.all == __o

    def __len__(self) -> int:
        return len(self._commits)
        
    def add(self, commit: Commit):
        if commit and commit not in self._commits:
            self._commits[commit.id] = commit
    
    def update(self, commits):
        for commit in commits:
            self.add(commit)

    def __sub__(self, other):
        return self.all - other.all

    @property
    def ids(self) -> Set[str]:
        return set(commit.id for commit in self._commits.values())

    @property
    def all(self) -> Set[Commit]:
        return set(commit for commit in self._commits.values())

    @property
    def authors(self) -> Set[str]:
        return set(commit.author for commit in self._commits.values())

    @property
    def committers(self) -> Set[str]:
        return set(commit.committer for commit in self._commits.values())

    def first(self, func: Callable = None) -> Commit:
        if self._commits:
            if func:
                ordered_commits = sorted(self._commits.values(), key=func)
            else:
                ordered_commits = list(self._commits.values())
            return ordered_commits[0]
        else:
            return None

    def last(self, func: Callable = None) -> Commit:
        if self._commits:
            if func:
                ordered_commits = sorted(self._commits.values(), key=func)
            else:
                ordered_commits = list(self._commits.values())
            return ordered_commits[-1]
        else:
            return None 