from releasy.models.commit import CommitGraph
from releasy.models.release import ReleaseGraph


class ProjectGraph:
    def __init__(self):
        self.releases = ReleaseGraph()
        self.commits = CommitGraph()