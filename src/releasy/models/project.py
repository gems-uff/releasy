
# Reintroduced ProjectGraph for backward compatibility with miners
from releasy.models.commit import CommitGraph
from releasy.models.release import ReleaseGraph

class ProjectGraph:
    def __init__(self):
        self.releases = ReleaseGraph()
        self.commits = CommitGraph()
from releasy.models.commit import CommitGraph
from releasy.models.release import ReleaseGraph

from .release import Release, ReleaseList



class ProjectGraph:
    def __init__(self):
        self.releases = ReleaseGraph()
        self.commits = CommitGraph()

class Project:
    """Represents a software project."""

    def __init__(self, name: str):
        self.name = name
        self.releases = ReleaseList()
