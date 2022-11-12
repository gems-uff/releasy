"""Commit Miner

This module mine commits and assign them to releases.

For each release, it assigns:
- its commits: the commits that belong to the release; and
- its tail commits: the first commits of each release branch
"""

from typing import Any, List, Tuple
from releasy.release import Release

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
        self.c2r = dict[Commit, Release]()

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        self.project = project
        self._mine_commits()
        return (self.project, [self.c2r])

    def _mine_commits(self) -> None:
        release_commits = set(map(lambda release: release.tag.commit, 
                              self.project.releases))

        releases = sorted(self.project.releases, 
                          key=lambda r: (r.time, r.version))
        for release in releases:
            commits = CommitSet()
            tails = CommitSet()
            loop_detector = set()
            commits_to_track: List[Commit] = [release.head]
            if release.head not in self.c2r:
                while commits_to_track:
                    commit = commits_to_track.pop()
                    commits.add(commit)
                    loop_detector.add(commit)

                    if commit not in self.c2r:
                        self.c2r[commit] = set()
                    self.c2r[commit].add(release)

                    if commit.parents:
                        for parent in commit.parents:
                            if parent not in release_commits \
                                    and not parent in self.c2r:
                                if parent not in loop_detector:
                                    commits_to_track.append(parent)
                            else:
                                tails.add(commit)
                    else:
                        tails.add(commit)

            release.tails = tails
            release.commits = commits
