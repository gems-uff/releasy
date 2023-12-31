from abc import ABC, abstractmethod
from typing import List, Self, Set

from releasy.project2 import Project
from releasy.release2 import Release, ReleaseVersioningSchema, SimpleVersioningSchema


class AMiner(ABC):
    def mine():
        pass


class ReferenceFilter(ABC):
    @abstractmethod
    def test(self, reference: str) -> bool:
        pass


class AllReferenceFilter(ReferenceFilter):
    def test(self, reference: str) -> bool:
        return True
    

class ReleaseFilter(ABC):
    @abstractmethod
    def test(self, release: str) -> bool:
        pass


class AllReleaseFilter(ReleaseFilter):
    def test(self, release: Release) -> bool:
       return True


class Repository(ABC):
    """ The Repository is an abstraction of any repository that contains
    information about releases, its changes, issues, and collaborators"""

    @property
    @abstractmethod
    def release_refs(self) -> List[str]:
        """ The references to the releases """
        pass
    

class ReleaseMiner():
    """ Mine releases in a repository """

    def __init__(
            self, 
            versioning_schema: ReleaseVersioningSchema = None,
            reference_filter: ReferenceFilter = None,
            release_filter: ReleaseFilter = None
            ) -> None:
        self.versioning_schema = versioning_schema or SimpleVersioningSchema()
        self.reference_filter = reference_filter or AllReferenceFilter()
        self.release_filter = release_filter or AllReleaseFilter()

    def mine(self, repository) -> Set[Release]:
        """ Mine the releases in a repository """

        release_refs = repository.release_refs
        filtered_refs = (ref for ref in release_refs 
                         if ref and self.reference_filter.test(ref))
        releases = (self.versioning_schema.apply(ref) for ref in filtered_refs)
        filtered_releases = (release for release in releases
                             if release and self.release_filter.test(release))
        return list(filtered_releases)


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
        