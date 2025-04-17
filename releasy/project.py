from releasy.commit import CommitGraph
from releasy.release import ReleaseGraph


class ProjectGraph:
    def __init__(self):
        self.releases = ReleaseGraph()
        self.commits = CommitGraph()
