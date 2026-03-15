from .commit import CommitList
from .release import ReleaseList


class Project:
    """Represents a software project."""

    def __init__(self, name: str = ""):
        self.name = name
        self.releases = ReleaseList()
        self.commits = CommitList()
