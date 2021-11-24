from typing import List
from datetime import timedelta

from .source import Datasource
from ..release import (
    Release,
    ReleaseSet)
from ..commit import Commit
from ..release import ContributorTracker


class AbstractCommitMiner:
    """ Mine release commits based on a strategy. It assign commits to 
    releases """

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params = None) -> ReleaseSet:
        raise NotImplementedError()


class HistoryCommitMiner(AbstractCommitMiner):
    """
    Implements the history-based strategy.

    It mines the releases considering the whole commit history. It walks through
    the commit parents to retrieve the commit history and split them based on
    the releases found in its history.
    """

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

