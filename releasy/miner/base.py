from abc import ABC, abstractmethod
from typing import List, Self, Set

from releasy.project2 import Project
from releasy.release2 import Release, SimpleVersioningSchema


class AMiner(ABC):
    def mine():
        pass
    
class SimpleReferenceFilter:
    def test(reference: str) -> bool:
        return True
    

class SimpleReleaseFilter:
    def test(release: Release) -> bool:
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
    def __init__(self) -> None:
        self.repository = None
        self.versioning_schema = SimpleVersioningSchema()
        self.reference_filter = SimpleReferenceFilter
        self.release_filter = SimpleReleaseFilter

    def mine(self, repository) -> Set[Release]:
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
        