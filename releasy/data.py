# Releasy Abstract data model
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .miner import AbstractReleaseMiner
    from typing import List

import re
   
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


class Release:
    """A single software release 
    
    :name: the release name
    :time: the release date
    :head: the last commit of the release
    """

    def __init__(self, name: ReleaseName, commit: Commit, time, description):
        self.name = name
        self.head = commit
        self.time = time
        self.description = description

    def __repr__(self):
        return repr(self.name)


class TagRelease(Release):
    """ A release represented by a tag """

    def __init__(self, tag: Tag, name: ReleaseName):
        super().__init__(name, tag.commit, tag.time, None) #TODO add description
        self.tag = tag


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

    def has_release(self) -> bool:
        return self.release != None

    def __repr__(self):
        return str(self.hashcode)


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


class ReleaseSet:
    """ An easy form to retrieve releases. It contains a set of releases, 
    its commits, and base releases"""
    def __init__(self):
        self.index = {}
        self.releases : List[ReleaseData] = []

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.releases[key]
        elif isinstance(key, str):
            return self.releases[self.index[key]]
        else: 
            raise TypeError()

    def add(self, release: Release, commits: List[Commit], 
            base_releases: List[ReleaseData] = None):

        data = ReleaseData(release, commits, base_releases)
        self.releases.append(data)
        self.index[release.name] = len(self.releases)-1

    def add_all(self, releases: List[ReleaseData]):
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


class ReleaseData:
    """ Connect release and commits """
    def __init__(self, release: Release = None, commits: List[Commit] = None, 
                 base_releases: List[ReleaseData] = None):
        self.release = release
        self.commits = commits
        self.base_releases = base_releases

    @property
    def merges(self):
        return set(commit for commit in self.commits if len(commit.parents) > 1)

    def __getattr__(self, name):
        if name in dir(self.release):
            return getattr(self.release, name)
        else:
            raise AttributeError

    def __repr__(self):
        return repr(self.name)


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
    

class Project:
    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        self.vcs = vcs
        self.releases = releases


### Utilities


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

    