from __future__ import annotations 

from datetime import datetime
from typing import Callable, TYPE_CHECKING

from releasy.models.commit import Commit, CommitList
from releasy.models.contributor import Contributor
from releasy.models.entity_list import EntityList

if TYPE_CHECKING:
    from releasy.version_format import ReleaseVersionFormat




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
                 message: str = None,
                 version_format: "ReleaseVersionFormat" | None = None,
    ) -> None:
        self.name = name
        self.timestamp = timestamp
        self.author = author
        self.head = head
        self.message = message
        self.previous = ReleaseList()
        self.next = ReleaseList()

        if version_format is None:
            from releasy.version_format import SemanticVersioningFormat

            version_format = SemanticVersioningFormat()
        version_parser = version_format
        self.version = version_parser.parse(name)

        self._commits: CommitList | None = None
        self._commits_loader: Callable[[], CommitList] | None = None

    @property
    def commits(self) -> CommitList:
        if self._commits is None:
            if self._commits_loader is not None:
                self._commits = self._commits_loader()
            else:
                self._commits = CommitList()
        return self._commits

    @commits.setter
    def commits(self, commits: CommitList) -> None:
        self._commits = commits

    def set_commits_loader(self, loader: Callable[[], CommitList]) -> None:
        self._commits_loader = loader
        self._commits = None

    @property
    def type(self):
        return self.version.type if self.version else None

    @property
    def base_releases(self) -> ReleaseList:
        return self.previous

    @base_releases.setter
    def base_releases(self, releases: ReleaseList) -> None:
        self.previous = releases

    def add_previous(self, base: 'Release'):
        if base is self:
            return
        if base not in self.previous:
            self.previous.append(base)
        if self not in base.next:
            base.next.append(self)

    def add_base_release(self, base: 'Release'):
        self.add_previous(base)

    def __repr__(self) -> str:
        return self.name


class ReleaseList(EntityList[Release]):
    """A list-like collection of releases supporting access by index or name."""

    def _key(self, item: Release) -> str:
        return item.name

    def names(self):
        return self.keys()