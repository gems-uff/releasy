# The Mine Strategy Module contains the core of releasy regarging the mining 
# releases and commits.
# 
#
#
from __future__ import annotations
from typing import Set, List

import re
from datetime import timedelta
from functools import cmp_to_key

from .metamodel import ContributorTracker, Developer, Commit, Datasource

from .release import (
    Release,
    TagRelease,
    ReleaseSet,
    ReleaseVersion
)

class ReleaseMatcher:
    """ Check if a name represent a release """

    def parse(self, name: str) -> ReleaseName:
        """
        :return: The release name or None if it is not a release
        """
        raise NotImplementedError()

class AbstractReleaseSorter:
    def sort(self, releases: ReleaseSet):
        raise NotImplementedError()

class ReleaseSorter(AbstractReleaseSorter):
    """ Sort releases according to a criteria """

    def sort(self, releases: ReleaseSet):
        if self._key_compare():
            sorted_internal_releases = sorted(releases, key=self._key)
        else: 
            sorted_internal_releases = sorted(releases, key=cmp_to_key(self._cmp))
        sorted_releases = ReleaseSet(sorted_internal_releases)

        prev_base_releases = []
        for release in sorted_releases:
            release.base_releases = prev_base_releases
            prev_base_releases = [release]

        return sorted_releases
        
    def _key_compare(self):
        return True

    def _key(self, release: Release):
        raise NotImplementedError()

    def _cmp(self, release: Release):
        raise NotImplementedError()


class AbstractReleaseMiner:
    """Mine releases bases on a strategy. It discover the releases. """
    matcher: ReleaseMatcher = None
    sorter: ReleaseSorter = None

    def mine_releases(self, datasource: Datasource) -> ReleaseSet:
        """ Mine the releases 

        :return: the list of releases
        """
        raise NotImplementedError()


class AbstractCommitMiner:
    """ Mine release commits based on a strategy. It assign commits to 
    releases """

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params = None) -> ReleaseSet:
        raise NotImplementedError()


class TrueReleaseMatcher(ReleaseMatcher):
    """ Matcher that consider all tags as releases """

    def parse(self, name: str) -> bool:
        return ReleaseName(name, None, None, None)


class VersionReleaseMatcher(ReleaseMatcher):
    """ Matcher that consider tags with version number as releases """
    def __init__(self, release_exceptions: List[str] = None):
        # TODO: define in a single object - repeated in VersionReleaseSorter
        self.version_regexp = re.compile(
            r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
        )
        self.release_exceptions = release_exceptions

    def parse(self, name: str) -> bool:
        if self.release_exceptions and name in self.release_exceptions:
            return None

        match = self.version_regexp.match(name)
        if match:
            prefix = match.group("prefix")
            version = match.group("version")
            suffix = match.group("suffix")
            return name
        else:
            return None


class VersionWoPreReleaseMatcher(VersionReleaseMatcher):
    """ Matcher that consider tags with version number as releases """
    def __init__(self, release_exceptions: List[str] = None, suffix_exception: str = None):
        super().__init__(release_exceptions=release_exceptions)
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

class DescribeReleaseSorter(AbstractReleaseSorter):
    """ Sort releases using git describe """
    def sort(self, releases: ReleaseSet):
        for release in releases:
            head_commit = release.head
            if head_commit.parents:
                base_release_name = head_commit.parents[0].describe()
                if base_release_name:
                    release.base_releases = [releases[base_release_name]]
                else:
                    release.base_releases = []
        return releases

class VersionReleaseSorter(ReleaseSorter):
    """ Sort release using its versions """
    def __init__(self):
        #TODO: define in a single object - repeated in VersionReleaseMatcher
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


class TimeVersionReleaseSorter(VersionReleaseSorter):
    def sort(self, releases: ReleaseSet):
        sorted_releases = super().sort(releases)
        for release in sorted_releases:
            if release.base_releases:
                base_release = release.base_releases[0] #TODO: consider multiple releases
                while base_release and release.time < base_release.time:
                    release.base_releases = base_release.base_releases
                    if release.base_releases:
                        base_release = release.base_releases[0]
                    else:
                        base_release = []
        return sorted_releases


# TODO: Return set of releases instead of ReleaseData
class TagReleaseMiner(AbstractReleaseMiner):
    """ Mine tags for releases """

    def mine_releases(self, datasource: Datasource) -> ReleaseSet:
        """ Discover releases """
        # Tags can reference any git object, but we just need the tags
        # that reference commits for release detection. 
        tags = [tag for tag in datasource.vcs.tags() if tag.commit]
        #tags = sorted(tags, key=lambda tag: tag.time, reverse=True)
        # TODO: sort releases
        releases = ReleaseSet()
        for tag in tags:
            release_name = self.matcher.parse(tag.name)
            if release_name:
                release = TagRelease(tag, release_name)
                releases.add(release)

        if self.sorter:
            releases = self.sorter.sort(releases)

        return releases


class HistoryCommitMiner(AbstractCommitMiner):
    """ Mine releases considering the whole commit history. It walks through 
    the commit parents to retrieve the commit history and split them based on 
    the releases found in its history.  """ 

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params = None):
        """ Assign the commits and base releases to the releases """
        assigned_commits = {}
        contributors = ContributorTracker()
        tagged_commits = {}
        for release in releases:
            if release.head.id not in tagged_commits:
                tagged_commits[release.head.id] = release

        for release in releases:
            contributors = ContributorTracker(contributors)
            commits, base_releases = self._track_commits(
                release, 
                assigned_commits, 
                contributors,
                tagged_commits
            )
            release.commits = commits
            release.contributors = contributors
            release.base_releases = base_releases

        for release in releases:    
            self._prune_commits(release)
        return releases

    def _track_commits(self, release: Release, 
            assigned_commits, 
            contributors: ContributorTracker, 
            tagged_commits) -> List[Commit]:
        """ Mine the reachable commits not assigned to other releases """
        # TODO: Check whether the commit is tagged by a release. 
        #       When a release has a wrong timestamp, it commit releases created
        #       after the actual release
        commit_loop = set()
        base_releases = ReleaseSet()
        
        commits = set()
        commits.add(release.head)
        commits_to_track = [parent_commit 
                            for parent_commit in release.head.parents]

        while commits_to_track:
            commit = commits_to_track.pop()
            commit_loop.add(commit)

            if commit not in commits:
                #TODO: released_commits
                if commit.id in tagged_commits:
                    base_release = tagged_commits[commit.id]
                    base_releases.add(base_release)
                else:
                    if commit.releases:
                        for r in commit.releases:
                            r.shared_commits.add(commit)
                        release.shared_commits.add(commit)
                    commit.releases.add(release)
                    commits.add(commit)
                    contributors.track(commit)
                    if commit.parents:
                        for parent_commit in commit.parents:
                            commits_to_track.append(parent_commit)

        return commits, base_releases

    def _prune_commits(self, release: Release):
        base_releases = set(release.base_releases)

        if release.shared_commits:
            releases_to_track = list(base_releases)
            while releases_to_track:
                cur_release = releases_to_track.pop()
                base_releases.add(cur_release)
                for base_release in cur_release.base_releases:
                    if base_release not in base_releases:
                        releases_to_track.append(base_release)

        for base_release in base_releases:
            release.commits -= base_release.commits

class TimeNaiveCommitMiner(AbstractCommitMiner):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params) -> ReleaseSet: 
        #TODO: handle order with release order
        commits = sorted(datasource.vcs.commits(), key=lambda commit: commit.committer_time) # error on vuejs v2.1.1
        
        for cur_release in releases:
            if cur_release.base_releases:
                base_release = cur_release.base_releases[0]
                prev_release_time = base_release.time
            else:
                prev_release_time = commits[0].committer_time - timedelta(1)

            cur_release_commits = set()
            for cur_commit in commits:
                if cur_commit.committer_time > prev_release_time and cur_commit.committer_time <= cur_release.time:
                    cur_release_commits.add(cur_commit)
            cur_release.commits = cur_release_commits
        return releases
       

class ReachableCommitMiner(AbstractCommitMiner):

    def _track_commits(self, head: Commit, start_time = None, include_self = False):
        """ return a list of all reachable commits from head made after start_time """
        ctrl = set()
        commits = set()
        commit_stack = [ head ]
        while commit_stack:
            commit = commit_stack.pop()
            if commit not in ctrl:
                if include_self:
                    if not start_time or commit.committer_time >= start_time:
                        commits.add(commit)
                else:
                    if not start_time or commit.committer_time > start_time:
                        commits.add(commit)

                for parent in commit.parents:
                    commit_stack.append(parent)
                ctrl.add(commit)
        return commits


class TimeCommitMiner(ReachableCommitMiner):
    """ Mine reachable commits until made after the previous release """

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params) -> ReleaseSet: 
        #TODO: handle order with release order

        for cur_release in releases:
            if cur_release.base_releases:
                base_release = cur_release.base_releases[0]
                prev_release_time = base_release.time
            else:
                prev_release_time = None

            cur_release_commits = self._track_commits(cur_release.head, prev_release_time)
            cur_release.commits = cur_release_commits
        return releases


class TimeExpertCommitMiner(TimeCommitMiner):
    """ Mine reachable commits until the first commit """

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params) -> ReleaseSet: 
        #TODO: handle order with release order

        for cur_release in releases:
            expert_cur_release = params["expert_release_set"][cur_release.name]
            if expert_cur_release.commits:
                first_commit = min(expert_cur_release.commits, key=lambda commit: commit.committer_time)
                first_commit_time = first_commit.committer_time
                cur_release_commits = self._track_commits(cur_release.head, first_commit_time, True)
            else:
                cur_release_commits = set()
            cur_release.commits = cur_release_commits

        return releases


class RangeCommitMiner(ReachableCommitMiner):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params) -> ReleaseSet:

        for cur_release in releases:
            if cur_release.base_releases:
                base_release = cur_release.base_releases[0]
                prev_release_history = self._track_commits(base_release.head)
            else:
                prev_release_history = set()

            cur_release_history = self._track_commits(cur_release.head)
            cur_release_commits = cur_release_history - prev_release_history
            cur_release.commits = cur_release_commits
        return releases


