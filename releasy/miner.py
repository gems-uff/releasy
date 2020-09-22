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
    def __init__(self, suffix_exception: str = None):
        super().__init__()
        if suffix_exception:
            self.suffix_exception = re.compile(suffix_exception)
        else:
            self.suffix_exception = None

    def parse(self, name: str) -> bool:
        release_name = super().parse(name)
        if release_name:
            if release_name.suffix == None:
                return release_name
            elif self.suffix_exception and self.suffix_exception.match(release_name.suffix):
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

        if r1.time > r2.time:
            return 1
        elif r1.time < r2.time:
            return -1
        else:
            return 0


# TODO Return set of releases instead of ReleaseData
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
            release_name = self. matcher.parse(tag.name)
            if release_name:
                release = TagRelease(tag, release_name)
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
            self.release_index[release.head.id] = release

        for release in self.releases:
            commits, base_releases = self._track_commits(release)
            releases.add(release.release, commits, base_releases)
        return releases
    
    def _track_commits(self, release: Release) -> List[Commit]:
        commits = []
        base_releases = set()
        commit_stack = [ release.head ]
        while len(commit_stack):
            commit = commit_stack.pop()
            if commit.id in self.commit_index:
                if self.commit_index[commit.id] != release:
                    base_releases.add(self.commit_index[commit.id])
            elif commit.id in self.release_index and commit.id != release.head.id:
                base_releases.add(self.release_index[commit.id])
            else:
                commits.append(commit)
                self.commit_index[commit.id] = release

                if commit.parents:
                    for parent in commit.parents:
                        commit_stack.append(parent)

        commits = sorted(commits, key=lambda commit: commit.committer_time, reverse=True)
        if not base_releases:
            base_releases = None
        return commits, base_releases


class TimeCommitMiner(AbstractCommitMiner):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        super().__init__(vcs, releases)
        self.release_index = {}
        
    def mine_commits(self) -> ReleaseSet: #TODO handle order with release order
        releases = ReleaseSet()
        commits = sorted(self.vcs.commits(), key=lambda commit: commit.committer_time)
        
        commit_index = {}
        for i,commit in enumerate(commits):
            commit_index[commit] = i

        start_commit_index = 0
        base_releases = []
        for cur_release in self.releases:
            end_commit_index = commit_index[cur_release.head]
            cur_release_commits = commits[start_commit_index:end_commit_index+1]
            releases.add(cur_release, cur_release_commits, base_releases)
            prev_release = cur_release
            start_commit_index = commit_index[prev_release.head]+1
            base_releases = [prev_release]

        return releases
       

class RangeCommitMiner(AbstractCommitMiner):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: ReleaseSet):
        super().__init__(vcs, releases)
        self._release_history = {}
        self._release_index = {}
        
    def mine_commits(self) -> ReleaseSet:
        releases = ReleaseSet()

        for cur_release in reversed(self.releases):
            self._release_index[cur_release.head.id] = cur_release

        prev_release_commits = set()
        base_releases = []
        for cur_release in self.releases:
            cur_release_history = self._track_commits(cur_release)
            self._release_history[cur_release.name] = cur_release_history
            cur_release_commits = cur_release_history - prev_release_commits
            releases.add(cur_release, cur_release_commits, base_releases)
            prev_release_commits = cur_release_history
            base_releases = [cur_release]
        return releases

    #TODO improve performance recording previous paths
    def _track_commits(self, release: Release):
        commit_index = {}
        commit_stack = [ release.head ]
        commits = set()
        while len(commit_stack):
            commit = commit_stack.pop()

            cached = False
            if commit != release.head and commit.id in self._release_index:
                reachable_release = self._release_index[commit.id]
                if reachable_release.name in self._release_history:
                    reachable_commits = self._release_history[reachable_release.name]
                    commits |= reachable_commits
                    cached = True
            
            if not cached:
                commits.add(commit)
                commit_index[commit] = True

                if commit.parents:
                    for parent in commit.parents:
                        if parent not in commit_index:
                            commit_stack.append(parent)
        return commits
