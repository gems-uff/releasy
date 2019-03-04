"""
Releasy Meta Model
"""

import re


class Project:
    """ Software Project"""

    def __init__(self):
        self.releases = []  #: list of project releases
                            #: regexp to match release name
        self.release_pattern = re.compile(r'(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?.*')


class Release:
    """Software Release

    Attributes:
        name (str): release name
        description (str): release description
        time: release creation time
        commits: list of commits that belong exclusively to this release
        tag: tag that represents the release
        head: commit referred  by release.tag
        tails: list of commits where the release begin
    """

    def __init__(self, tag):
        self.tag = tag
        self.commits = []
        self.tails = []

    @property
    def name(self):
        return self.tag.name

    @property
    def description(self):
        return self.tag.message

    @property
    def time(self):
        return self.tag.time

    @property
    def head(self):
        return self.tag.commit


class Tag:
    """Tag

    Attributes:
        name: tag name
        commit: tagged commit
        time: tag time
        message (str): tag message - annotated tags only
    """

    def __init__(self):
        self.name = None
        self.commit = None
        self.time = None
        self.message = None


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
        self.release = None


class Contributor:
    """ Developers and committers """

    def __init__(self):
        self.name = None    #: contributor name
        self.email = None   #: contributor e-mail
