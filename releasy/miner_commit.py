"""Commit Miner

This module mine commits and assign them to releases.

For each release, it assigns:
- its commits: the commits that belong to the release; and
- its tail commits: the first commits of each release branch
"""

from typing import Any, List, Tuple
from releasy.release import Commit2ReleaseMapper, Release

from releasy.repository import Commit, CommitSet
from .miner_base import AbstractMiner
from .project import Project


class MixedHistoryCommitMiner(AbstractMiner):
    def __init__(self) -> None:
        super().__init__()
        self.c2r = dict[Commit, Release]()

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project
        self._mine_commits()
        return (self.project, [self.c2r])

    def _mine_commits(self) -> None:
        release_commits = set(map(lambda release: release.tag.commit, 
                              self.project.releases))

        for release in self.project.releases:
            commits = CommitSet()
            tails = CommitSet()
            loop_detector = set()
            commits_to_track: List[Commit] = [release.head]

            if release.head not in self.c2r:
                self.c2r[release.head] = set()
            self.c2r[release.head].add(release)

            while commits_to_track:
                commit = commits_to_track.pop()
                commits.add(commit)
                loop_detector.add(commit)

                if commit.parents:
                    for parent in commit.parents:
                        if parent not in release_commits:
                            if parent not in loop_detector:
                                commits_to_track.append(parent)
                        else:
                            tails.add(commit)
                else:
                    tails.add(commit)

            release.tails = tails
            release.commits = commits


class HistoryCommitMiner(AbstractMiner):
    
    def __init__(self) -> None:
        super().__init__()
        self.c2r = Commit2ReleaseMapper()

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project
        self._assign_heads()
        self._mine_releases()
        return (self.project, [self.c2r]) 

    def _assign_heads(self):
        for release in sorted(
                self.project.releases, 
                key=lambda r: (r.time, r.version)):
            if not self.c2r.get_release(release.head):
                self.c2r.assign_commit(release.head, release)

    def _mine_releases(self) -> None:
        for release in sorted(
                self.project.releases, 
                key=lambda r: (r.time, r.version)):
            commits, tails = self._mine_commits(release)
            release.commits = commits
            release.tails = tails

    def _mine_commits(self, release):
        commit = release.head

        commit_release = self.c2r.get_release(commit) 
        if commit_release and release not in commit_release:
            return CommitSet(), CommitSet()
        
        commits = CommitSet()
        tails = CommitSet()
        commits_to_track: List[Commit] = [commit]    
        while commits_to_track:
            commit = commits_to_track.pop()
            
            self.c2r.assign_commit(commit, release)
            commits.add(commit)

            if not commit.parents:
                tails.add(commit)

            for parent in commit.parents:
                if not self.c2r.get_release(parent):
                    commits_to_track.append(parent)
                else:
                    tails.add(commit)
                    
        return commits, tails
    
