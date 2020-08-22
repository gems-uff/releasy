# The Mine Strategy Module contains the core of releasy regarging the mining 
# releases and commits.
# 
#
#
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List

import re

from .release import Release
from .model import Tag, Commit
from .miner.vcs.miner import Vcs
from .data import Release


class ReleaseMatcher:
    """ Check if an object is a release """

    def is_release(self, object) -> bool:
        """
        :return: True if the object is a release
        """
        pass


class ReleaseSorter:
    """ Sort releases according to a criteria """

    def sort(self, releases):
        pass


class ReleaseMineStratety:
    """Mine releases bases on a strategy. It discover the releases. """

    def __init__(self, vcs: Vcs, matcher: ReleaseMatcher, sorter: ReleaseSorter):
        self.vcs = vcs
        self.matcher = matcher
        self.sorter = sorter

    def mine_releases(self) -> List[Release]:
        """ Mine the releases 

        :return: the list of releases in reverse cronological order
        """
        pass


class CommitMineStrategy:
    """ Mine release commits based on a strategy. It assign commits to 
    releases """

    def __init__(self, vcs: Vcs, releases: List[Release]):
        self.vcs = vcs
        self.releases = releases

    def mine_commits():
        pass


class TrueReleaseMatcher:
    """ Matcher that consider all tags as releases """

    def is_release(self, tag: Tag) -> bool:
        return True


class VersionReleaseMatcher(ReleaseMatcher):
    """ Matcher that consider tags with version number as releases """
    def __init__(self):
        self.version_regexp = re.compile(
            r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
        )

    def is_release(self, tag: Tag) -> bool:
        if self.version_regexp.match(tag.name):
            return True
        else:
            return False


class TimeReleaseSorter(ReleaseSorter):
    """ Sort releases using time """
    def sort(self, releases):
        sorted_releases = sorted(releases, key=lambda release: release.time)
        return sorted_releases


class VersionReleaseSorter(ReleaseSorter):
    """ Sort release using its versions """

    def sort(self):
        pass


class TagReleaseMineStrategy(ReleaseMineStratety):
    """ Mine tags for releases """

    def __init__(self, vcs: Vcs, release_matcher: ReleaseMatcher, 
            release_sorter: ReleaseSorter):
        super().__init__(vcs, release_matcher, release_sorter)

    def mine_releases(self) -> List[Release]:
        """ Discover releases """
        # Tags can reference any git object. For release detectioin purpouse, 
        # we only need tags that reference commits
        tags = [tag for tag in self.vcs.tags() if tag.commit]
        #tags = sorted(tags, key=lambda tag: tag.time, reverse=True)
        releases = []
        for tag in tags:
            if self.matcher.is_release(tag):
                release = Release(tag)
                releases.append(release)

        sorted_releases = self.sorter.sort(releases)
        return sorted_releases


class PathMineStrategy(CommitMineStrategy):
    """ Mine releases based on the commit history. It walk through the commit
    parents to retrieve the commit history and split them based on the 
    releases found in its history. """ 

    def __init__(self, vcs: Vcs, releases: List[Release]):
        super().__init__(vcs, releases)
        self.release_index = {}
        self.commit_index = {}

    def mine_commits(self):
        releases = sorted(self.releases, key=lambda release: release.time)
        for release in releases:
            self.release_index[release.head.id] = True

        release_commits = {}
        for release in releases:
            commits = self._track_commits(release)
            release_commits[release.name] = commits
        return release_commits
    
    def _track_commits(self, release: Release) -> List[Commit]:
        commits = []
        commit_stack = [ release.head ]
        while len(commit_stack):
            commit = commit_stack.pop()
            if commit.id not in self.commit_index:
                commits.append(commit)
                self.commit_index[commit.id] = True

                if commit.parents:
                    for parent in commit.parents:
                        if not parent.id in self.release_index:
                            commit_stack.append(parent)

        commits = sorted(commits, key=lambda commit: commit.committer_time, reverse=True)
        return commits


class TimeMineStrategy(CommitMineStrategy):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: List[Release]):
        super().__init__(vcs, releases)
        self.release_index = {}
        
    def mine_commits(self):
        releases = sorted(self.releases, key=lambda release: release.time)
        commits = sorted(self.vcs.commits(), key=lambda commit: commit.committer_time)

        release_commits = {}
        commit_index = 0
        release_index = 0

        has_releases = True
        while has_releases:
            cur_release = releases[release_index]
            cur_release_commits = []
            
            has_commits = True
            while has_commits:
                cur_commit = commits[commit_index]
                
                if cur_commit.committer_time <= cur_release.time:
                    cur_release_commits.append(cur_commit)
                    commit_index += 1
                else:
                    has_commits = False
                
                if commit_index >= len(commits):
                    has_commits = False

            cur_release_commits = sorted(cur_release_commits, key=lambda commit: commit.committer_time, reverse=True)
            release_commits[cur_release.name] = cur_release_commits        
            release_index += 1
            if release_index >= len(releases):
                has_releases = False

        return release_commits


class RangeMineStrategy(CommitMineStrategy):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: List[Release]):
        super().__init__(vcs, releases)
        self.release_index = {}
        
    def mine_commits(self):
        pass
