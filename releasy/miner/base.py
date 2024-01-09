from abc import ABC, abstractmethod
from typing import Callable, List, Self, Set
from releasy.miner.repository import Repository

from releasy.project2 import Project
from releasy.release2 import Release, ReleaseBuilder, ReleaseReference, ReleaseVersioningSchema, SimpleVersioningSchema


class ReleaseMiner():
    """ Mine releases in a repository """

    def __init__(
            self, 
            versioning_schema: ReleaseVersioningSchema = None,
            reference_filter: Callable[[ReleaseReference], bool] = None,
            release_filter: Callable[[Release], bool] = None
        ) -> None:
        self.versioning_schema = versioning_schema or SimpleVersioningSchema()
        self.release_builder = ReleaseBuilder(self.versioning_schema)
        self.reference_filter = reference_filter or no_filter
        self.release_filter = release_filter or no_filter

    def mine(self, repository: Repository) -> Set[Release]:
        """ Mine the releases in a repository """
        return [
            release for release in (
                self.release_builder.reference(ref).build() 
                for ref in repository.release_refs
                if ref and self.reference_filter(ref)
            )
            if release and self.release_filter(release)
        ]


def no_filter(value):
    """ Dummy filter that always return True """
    return True


class Miner:
    def __init__(self, path: str, project: Project = None) -> None:
        self.path = path
        self.project = project
        self.miners = []

    def apply(self) -> Self:
        return self
    
    def mine() -> Project:
        pass

# releasy.Miner("/", project)
#        .apply(GitMiner)
#        .apply(FinalReleaseOnly)
#        .apply(SemanticVersion)
#        .apply(HistoryBased)
#        .mine()
        