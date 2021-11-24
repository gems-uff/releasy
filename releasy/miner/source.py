

from typing import List

from ..commit import (
    Commit, 
    Tag)

class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """
    def __init__(self, path):
        self.path = path
        self._tags = []

    def tags(self) -> List[Tag]:
        """ Return repository tags """
        return self._tags

    def commits(self) -> List[Commit]:
        pass


class Datasource():
    def __init__(self, **kwargs) -> None:
        self.vcs: Vcs = None
        if 'vcs' in kwargs:
            self.vcs = kwargs['vcs']
