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
from datetime import timedelta
from functools import cmp_to_key

from .data import Tag, Commit, Release, TagRelease, Vcs, ReleaseSet, ReleaseName


class ReleaseMatcher:
    """ Check if a name represent a release """

    def parse(self, name: str) -> ReleaseName:
        """
        :return: The release name or None if it is not a release
        """
        raise NotImplementedError()


class ReleaseSorter:
    """ Sort releases according to a criteria """

    def sort(self, releases: ReleaseSet):
        internal_releases = releases.get_all()
        if self._key_compare():
            sorted_internal_releases = sorted(internal_releases, key=self._key)
        else: 
            sorted_internal_releases = sorted(internal_releases, key=cmp_to_key(self._cmp))
        sorted_releases = ReleaseSet()
        sorted_releases.add_all(sorted_internal_releases)
        return sorted_releases
        
    def _key_compare(self):
        return True

    def _key(self, release: Release):
        raise NotImplementedError()

    def _cmp(self, release: Release):
        raise NotImplementedError()


class AbstractReleaseMiner:
    """Mine releases bases on a strategy. It discover the releases. """

    def __init__(self, vcs: Vcs, matcher: ReleaseMatcher, sorter: ReleaseSorter):
        self.vcs = vcs
        self.matcher = matcher
        self.sorter = sorter

    def mine_releases(self) -> ReleaseSet:
        """ Mine the releases 

        :return: the list of releases in reverse cronological order
        """
        raise NotImplementedError()


class AbstractCommitMiner:
    """ Mine release commits based on a strategy. It assign commits to 
    releases """

    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        self.vcs = vcs
        self.releases = releases

    def mine_commits(self) -> ReleaseSet:
        raise NotImplementedError()


class TrueReleaseMatcher(ReleaseMatcher):
    """ Matcher that consider all tags as releases """

    def parse(self, name: str) -> bool:
        return ReleaseName(name, None, None, None)


class VersionReleaseMatcher(ReleaseMatcher):
    """ Matcher that consider tags with version number as releases """
    def __init__(self):
        # TODO define in a single object - repeated in VersionReleaseSorter
        self.version_regexp = re.compile(
            r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
        )

    def parse(self, name: str) -> bool:
        match = self.version_regexp.match(name)
        if match:
            prefix = match.group("prefix")
            version = match.group("version")
            suffix = match.group("suffix")
            return ReleaseName(name, prefix, version, suffix)
        else:
            return None


class VersionWoPreReleaseMatcher(VersionReleaseMatcher):
    """ Matcher that consider tags with version number as releases """
    def __init__(self):
        super().__init__()

    def parse(self, name: str) -> bool:
        release_name = super().parse(name)
        if release_name and release_name.suffix == None:
            return release_name
        else:
            return None


class TimeReleaseSorter(ReleaseSorter):
    """ Sort releases using time """
    def _key(self, release: Release):
        return release.time


class VersionReleaseSorter(ReleaseSorter):
    """ Sort release using its versions """
    def __init__(self):
        # TODO define in a single object - repeated in VersionReleaseMatcher
        self.version_regexp = re.compile(
            r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
        )
        self.version_sep = re.compile(r"[\._]")
        self.pre_release_sep = re.compile(r"(?P<name>[^0-9]*)?(?P<number>[0-9]*)?")

    def _key_compare(self):
        return False

    def _tokenize(self, release: Release):
        name = release.name
        match = self.version_regexp.match(name)
        version = match.group("version")
        suffix = match.group("suffix")
        tokens = self.version_sep.split(version)
        for part in self.version_sep.split(suffix):
            sep = self.pre_release_sep.match(part)
            if sep and sep.group("name"):
                tokens.append(sep.group("name"))
            if sep and sep.group("number"):
                tokens.append(sep.group("number"))
        return tokens

    def _get_token(self, tokens, position):
        if position < len(tokens):
            token_value = tokens[position]
            token_is_number = token_value.isdigit()
            if token_is_number:
                token_value = int(token_value)
        else:
            token_value = 0
            token_is_number = True
        return (token_value, token_is_number)

    def _cmp(self, r1: Release, r2: Release):
        tk1 = self._tokenize(r1)
        tk2 = self._tokenize(r2)

        # Compare versions
        i = 0
        while i < max(len(tk1), len(tk2)):
            (c1, c1_is_number) = self._get_token(tk1, i)
            (c2, c2_is_number)= self._get_token(tk2, i)

            if c1_is_number and c2_is_number:
                cmp = c1 - c2
                if cmp != 0:
                    return cmp
            elif c1_is_number and not c2_is_number:
                return 1
            elif not c1_is_number and c2_is_number:
                return -1
            else:
                if c1 > c2:
                    return  1
                elif c1 < c2:
                    return -1
            i += 1
        return 0



class TagReleaseMiner(AbstractReleaseMiner):
    """ Mine tags for releases """

    def __init__(self, vcs: Vcs, release_matcher: ReleaseMatcher, 
            release_sorter: ReleaseSorter):
        super().__init__(vcs, release_matcher, release_sorter)

    def mine_releases(self) -> ReleaseSet:
        """ Discover releases """
        # Tags can reference any git object. For release detectioin purpouse, 
        # we only need tags that reference commits
        tags = [tag for tag in self.vcs.tags() if tag.commit]
        #tags = sorted(tags, key=lambda tag: tag.time, reverse=True)
        releases = ReleaseSet()
        for tag in tags:
            if self. matcher.parse(tag.name):
                release = TagRelease(tag)
                releases.add(release, None)

        #TODO use ReleaseSet
        sorted_releases = self.sorter.sort(releases)
        return sorted_releases


class PathCommitMiner(AbstractCommitMiner):
    """ Mine releases based on the commit history. It walk through the commit
    parents to retrieve the commit history and split them based on the 
    releases found in its history. """ 

    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        super().__init__(vcs, releases)
        self.release_index = {}
        self.commit_index = {}

    def mine_commits(self):
        releases = ReleaseSet()
        for release in self.releases:
            self.release_index[release.head.id] = True

        for release in self.releases:
            commits = self._track_commits(release)
            releases.add(release.release, commits)
        return releases
    
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


class TimeCommitMiner(AbstractCommitMiner):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        super().__init__(vcs, releases)
        self.release_index = {}
        
    def mine_commits(self) -> ReleaseSet: #TODO handle order with release order
        releases = ReleaseSet()
        commits = sorted(self.vcs.commits(), key=lambda commit: commit.committer_time)

        start = commits[0].committer_time - timedelta(days=1)
        for cur_release in self.releases:
            end = cur_release.time

            cur_release_commits = []
            for commit in commits:
                if commit.committer_time > start and commit.committer_time <= end:
                    cur_release_commits.append(commit)
            releases.add(cur_release, cur_release_commits)     

            prev_release = cur_release
            start = prev_release.time
        return releases


class RangeCommitMiner(AbstractCommitMiner):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        super().__init__(vcs, releases)
        
    def mine_commits(self) -> ReleaseSet:
        releases = ReleaseSet()
        prev_commit_set = set()
        for release in self.releases:
            cur_commit_set = self._track_commits(release)
            range_commit_set = cur_commit_set - prev_commit_set
            releases.add(release, list(range_commit_set))
            prev_commit_set = cur_commit_set
        return releases

    #TODO improve performance recording previous paths
    def _track_commits(self, release: Release):
        commit_index = {}
        commit_stack = [ release.head ]
        commits = set()
        while len(commit_stack):
            commit = commit_stack.pop()
            commits.add(commit)
            commit_index[commit] = True

            if commit.parents:
                for parent in commit.parents:
                    if parent not in commit_index:
                        commit_stack.append(parent)
        return commits
