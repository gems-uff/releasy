from __future__ import annotations 

from datetime import datetime

from releasy.models.commit import Commit, CommitList
from releasy.models.contributor import Contributor




class Release:
    """
    A Release is a group of commits ready to be delivered to its stakeholders.
    Lightweight: only name, timestamp, author, head, message. Version is lazy/optional.
    """

    def __init__(self,
                 name: str,
                 timestamp: datetime,
                 author: Contributor,
                 head: Commit,
                 message: str = None
    ) -> None:
        self.name = name
        self.timestamp = timestamp
        self.author = author
        self.head = head
        self.message = message
        self.base_releases = ReleaseList()
        self.commits = CommitList()
        self.version = None

    def add_base_release(self, base: 'Release'):
        if base not in self.base_releases:
            self.base_releases.append(base)

    def __repr__(self) -> str:
        return self.name


class ReleaseList:
    """A list-like collection of releases supporting access by index or name."""
    def __init__(self, releases=None):
        self._releases = [] if releases is None else list(releases)
        self._by_name = {r.name: r for r in self._releases}

    def append(self, release):
        self._releases.append(release)
        self._by_name[release.name] = release

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._releases[key]
        elif isinstance(key, str):
            return self._by_name[key]
        else:
            raise TypeError("ReleaseList indices must be int or str (name)")

    def __iter__(self):
        return iter(self._releases)

    def __len__(self):
        return len(self._releases)

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._by_name
        return item in self._releases

    def names(self):
        return list(self._by_name.keys())