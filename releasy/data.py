# Releasy Abstract data model

from .model import Tag



class Release:
    """A single software release 
    
    :name: the release name
    :time: the release date
    :head: the last commit of the release
    """

    def __init__(self, tag: Tag):
        self._tag = tag
        self.name = tag.name
        self.time = tag.time
        self.head = tag.commit


    def __repr__(self):
        return self.name


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """
    def __init__(self, path):
        self.path = path
        self._tags = []

    def tags(self):
        """ Return repository tags """
        return self._tags

    def commits(self):
        pass


