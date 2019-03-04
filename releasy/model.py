"""
Releasy Meta Model
"""

class Project:
    """ Software Project"""

    def __init__(self):
        self.releases = []


class Release:
    """ Software Release """

    def __init__(self):
        self.commits = []   #: list of commits that belong exclusively to this release
        self.tag = None     #: tag that represents the release
        self.head = None    #: commit referred  by release.tag
        self.tails = []     #: list of commits where the release begin


class Tag:
    """ Tag """

    def __init__(self):
        self.name = None    #: tag name
        self.commit = None  #: tagged commit

class Commit:
    """ Commit """

    def __init__(self):
        self.id = None          #: commit id
        self.parents = []       #: previous commits
        self.children = []      #: next commits
        self.subject = None     #: first line from commit message
        self.message = None     #: commit message
        self.committer = None   #: contributor responsible for the commit
        self.author = None      #: contributor responsible for the code


class Contributor:
    """ Developers and committers """

    def __init__(self):
        self.name = None    #: contributor name
        self.email = None   #: contributor e-mail
