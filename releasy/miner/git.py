from typing import Set

import pygit2

from releasy.miner.base import ReleaseMiner
from releasy.release2 import Release, ReleaseBuilder


class GitRepository:
    pass


class GitReleaseMiner(ReleaseMiner):
    def __init__(self, repository: GitRepository, ) -> None:
        super().__init__()
        self.git = repository

    def mine(self) -> Set[Release]:
        tags = [ref for ref in self.git.references.objects 
                    if ref.name.startswith('refs/tags/')]

        release_builder = ReleaseBuilder()
        releases = map(
            lambda tag: release_builder.name(tag.shorthand).build(),
            tags)
        return list(releases)
