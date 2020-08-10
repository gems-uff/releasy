#
#
#
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

