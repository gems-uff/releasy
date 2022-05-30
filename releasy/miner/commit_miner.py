from abc import ABC, abstractmethod
from typing import List, Set
from datetime import timedelta

from .source import Datasource
from ..release_old import (
    Release,
    ReleaseSet)
from ..commit import Commit
from ..release_old import ContributorTracker


class CommitMiner(ABC):
    """ Mine release commits based on a strategy. It assign commits to 
    releases """

    @abstractmethod
    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params = None) -> ReleaseSet:
        """ Assign the commits and base releases to the releases """
        raise NotImplementedError()


class HistoryCommitMiner(CommitMiner):
    """
    Implements the history-based strategy.

    It mines the releases considering the whole commit history. It walks through
    the commit parents to retrieve the commit history and split them based on
    the releases found in its history.
    """

    def mine_commits(self, datasource: Datasource, releases: ReleaseSet,
            params = None):
        for release in releases:
            self._mine_release_history(release)

        for release in releases:    
            self._prune_commits(release)
        return releases

    def _mine_release_history(self, release: Release):
        commits_to_track: List[Commit] = [parent_commit for parent_commit 
                                                        in release.head.parents]
        while commits_to_track:
            commit = commits_to_track.pop()
            if commit not in release.commits:
                if not commit.head_releases:
                    release.add_commit(commit)
                    if commit.parents:
                        commits_to_track.extend(commit.parents)
                else:
                    release.base_releases.update(commit.head_releases)

    def _prune_commits(self, release: Release):
        """Remove commits reachable by base releases"""
        #TODO unset has_shared_commits
        base_releases: Set[Release] = set()
        if release.has_shared_commits and release.base_releases:
            base_releases_to_track = list(release.base_releases)
            while base_releases_to_track:
                base_release = base_releases_to_track.pop()
                if base_release not in base_releases:
                    base_releases.add(base_release)
                    if base_release.base_releases:
                        base_releases_to_track.extend(base_release.base_releases)
            
        for base_release in base_releases:
            commits_to_remove = release.commits & base_release.commits
            if commits_to_remove:
                for base_base_release in base_release.base_releases:
                    release.remove_base_release(base_base_release)
                for commit in commits_to_remove:
                    release.remove_commit(commit)


class TimeNaiveCommitMiner(CommitMiner):
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
       

class ReachableCommitMiner(CommitMiner):

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

