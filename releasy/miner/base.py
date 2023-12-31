from abc import ABC, abstractmethod
from typing import List, Self, Set
from releasy.miner.repository import Repository

from releasy.project2 import Project
from releasy.release2 import Release, ReleaseBuilder, ReleaseVersioningSchema, SimpleVersioningSchema


class ReferenceFilter(ABC):
    """ Filter references before parsing the release """
    @abstractmethod
    def test(self, reference: str) -> bool:
        pass


class AllReferenceFilter(ReferenceFilter):
    """ Select all references """
    def test(self, reference: str) -> bool:
        return True
    

class ReleaseFilter(ABC):
    """ Filter releases """
    @abstractmethod
    def test(self, release: str) -> bool:
        pass


class AllReleaseFilter(ReleaseFilter):
    """ Select all releases """
    def test(self, release: Release) -> bool:
       return True


class ReleaseMiner():
    """ Mine releases in a repository """

    def __init__(
            self, 
            versioning_schema: ReleaseVersioningSchema = None,
            reference_filter: ReferenceFilter = None,
            release_filter: ReleaseFilter = None) -> None:
        self.versioning_schema = versioning_schema or SimpleVersioningSchema()
        self.release_builder = ReleaseBuilder(self.versioning_schema)
        self.reference_filter = reference_filter or AllReferenceFilter()
        self.release_filter = release_filter or AllReleaseFilter()

    def mine(self, repository: Repository) -> Set[Release]:
        """ Mine the releases in a repository """

        release_refs = repository.release_refs
        filtered_refs = [
            ref for ref in release_refs 
            if ref and self.reference_filter.test(ref)]
        releases = [
            self.release_builder.reference(ref).build() 
            for ref in filtered_refs]
        filtered_releases = [
            release for release in releases
            if release and self.release_filter.test(release)]
        return filtered_releases


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
        