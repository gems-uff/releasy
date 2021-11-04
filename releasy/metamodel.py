from __future__ import annotations
from typing import List, Set

import re


class Project():
    
    def __init__(self) -> None:
        self.releases: ReleaseSet = None
        self.datasource: Datasource = None


class ReleaseSet:
    """ An easy form to retrieve releases. It contains a set of releases, 
    its commits, and base releases"""
    def __init__(self):
        self.index = {}
        self.releases : List[Release] = []

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.releases[key]
        elif isinstance(key, str):
            return self.releases[self.index[key]]
        else: 
            raise TypeError()

    def add(self, release: Release):
        self.releases.append(release)
        self.index[release.name] = len(self.releases)-1

    def add_all(self, releases: List[Release]):
        for release in releases:
            self.releases.append(release)
            self.index[release.name] = len(self.releases)-1

    def get_all(self):
        return self.releases

    @property
    def prefixes(self):
        """ return a set with all the release prefixes, including None if there
        is at least one release withou prefix """
        prefixes = FrequencySet()
        for release in self.releases:
            prefixes.add(release.name.prefix)
        return prefixes

    @property
    def suffixes(self):
        """ return a set with all the release suffixes """
        suffixes = FrequencySet()
        for release in self.releases:
            suffixes.add(release.name.suffix)
        return suffixes

    def __len__(self):
      return len(self.releases)


class Release:
    """A software release"""

    def __init__(self, name: ReleaseName, commit: Commit, time, description):
        self.name = name
        self.head = commit
        self.time = time
        self.description = description
        self.commits: Set[Commit] = set([self.head])
        self.base_releases: Set[Release] = set()
        self.contributors : ContributorTracker = ContributorTracker()

    def __hash__(self):
        return hash((self.name, self.head))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        return False

    def __repr__(self):
        return repr(self.name)

    @property
    def merges(self):
        return set(commit for commit in self.commits if len(commit.parents) > 1)


class TagRelease(Release):
    """ A release represented by a tag """

    def __init__(self, tag: Tag, name: ReleaseName):
        super().__init__(name, tag.commit, tag.time, None) #TODO add description
        self.tag = tag


class ReleaseName(str):
    """ Represent a release name, with prefix, version and suffix """
    def __init__(self, name: str, prefix: str, version: str, suffix: str):
        if not name:
            raise ValueError("release name must have a non empty name")
        self.value = name
        self.prefix = prefix or None
        self.version = version or None
        self.suffix = suffix or None

    @property
    def semantic_version(self):
        """ Return 3 first version numbers separated by dot. Add 0 to missing 
        version and remove version number beyond 3 """
        
        version_sep = re.compile(r"[\._]")

        if not self.version:
            return None
        
        version_part = version_sep.split(self.version)
        version_part_cnt = len (version_part)

        for i in range(3 - version_part_cnt):
            version_part.append("0")
        return f"{version_part[0]}.{version_part[1]}.{version_part[2]}"

    def __new__(self, name, *args, **kwargs):
        return super().__new__(self, name)

    def __hash__(self):
        return hash(self.value)


class FrequencySet(set):
    def __init__(self):
        self._count = {}

    def add(self, value):
        super().add(value)
        if value not in self._count:
            self._count[value] = 1
        else:
            self._count[value] += 1

    def count(self, value):
        return self._count[value]

    def mode(self):
        max_count = 0
        max_value = None
        for value in self._count:
            if self._count[value] > max_count:
                max_count = self._count[value]
                max_value = value
        return max_value


class Tag:
    """Tag

    Attributes:
        name: tag name
        commit: tagged commit
        time: tag time
        message (str): tag message - annotated tags only
    """

    def __init__(self, name, commit, time=None, message=None):
        self.name = name
        self.commit = commit
        self.release = None
        self.time = None
        self.message = None
        if time: # annotated tag
            self.is_annotated = True
            self.time = time
            self.message = message
        else:
            self.is_annotated = False
            if commit:
                self.time = commit.committer_time
                self.message = commit.message
    
    def __repr__(self):
        return self.name


class Commit:
    """
    Commit

    Attributes:
        hashcode: commit id
        message: commit message
        subject: first line from commit message
        committer: contributor responsible for the commit
        author: contributor responsible for the code
        time: commit time
        author_time: author time
        release: associated release
    """
    def __init__(self, hashcode, parents=None, message=None, 
                 author=None, author_time=None, 
                 committer=None, committer_time=None):
        self.id = hashcode
        self.hashcode = hashcode
        self.parents = parents
        self.message = message
        self.author = author
        self.author_time = author_time
        self.committer = committer
        self.committer_time = committer_time
        self.release = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        return False

    def has_release(self) -> bool:
        return self.release != None

    def __repr__(self):
        return str(self.hashcode)

    def describe(self):
        raise NotImplementedError()


class Developer:
    """
    Project Contributors

    Attributes:
        login: developer id
        name: developer name
        email: developer e-mail
    """

    def __init__(self, login, name, email):
        self.login = login
        self.name = name
        self.email = email

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, obj):
        if isinstance(obj, Developer):
            if self.login == obj.login:
                return True
        return False

    def __repr__(self):
        return self.login


class ContributorTracker():
    """ Track developers' contributions to a release """
    def __init__(self, tracked_contributors: ContributorTracker = None):
        self.authors = set()
        self.committers = set()
        self.newcomers = set()
        self.tracked_contributors = set()
        if tracked_contributors:
            self.tracked_contributors = tracked_contributors.tracked_contributors

    def track(self, commit: Commit):
        author = commit.author
        committer = commit.committer
        self.authors.add(author)
        self.committers.add(committer)
        if committer not in self.tracked_contributors:
            self.newcomers.add(committer)
            self.tracked_contributors.add(committer)
        if author not in self.tracked_contributors:
            self.newcomers.add(author)
            self.tracked_contributors.add(author)


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
    vcs: Vcs = None
    releases: ReleaseSet = None

    def __init__(self, **kwargs) -> None:
        if 'vcs' in kwargs:
            self.vcs = kwargs['vcs']


