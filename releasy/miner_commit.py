"""Commit Miner

This module mine commits and assign them to releases.

For each release, it assigns:
- its commits: the commits that belong to the release; and
- its tail commits: the first commits of each release branch
"""

from typing import List
from releasy.release import Release

from releasy.repository import Commit, CommitSet
from .miner_base import AbstractMiner
from .project import Project


class MixedHistoryCommitMiner(AbstractMiner):
    def __init__(self) -> None:
        super().__init__()
        self.c2r = dict[Commit, Release]()

    def mine(self) -> Project:
        self._mine_commits()
        self._mine_base_releases()
        return self.project

    def _mine_commits(self) -> None:
        release_commits = set(map(lambda release: release.tag.commit, 
                              self.project.releases))

        for release in self.project.releases:
            commits = CommitSet()
            tails = CommitSet()
            loop_detector = set()
            commits_to_track: List[Commit] = [release.head]
            while commits_to_track:
                commit = commits_to_track.pop()
                commits.add(commit)
                loop_detector.add(commit)

                if commit not in self.c2r:
                    self.c2r[commit] = set()
                self.c2r[commit].add(release)

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

    def _mine_base_releases(self) -> None:
        for release in self.project.releases:
            for tail in release.tails:
                for parent in tail.parents:
                    if parent in self.c2r:
                        for base_release in self.c2r[parent]:
                            if base_release != release \
                                    and base_release.head != release.head:
                                release.base_releases.update(self.c2r[parent])
        return self.project


class HistoryCommitMiner(AbstractMiner):
    def __init__(self) -> None:
        super().__init__()
        self.c2r = dict[Commit, Release]()

    def mine(self) -> Project:
        self._mine_commits()
        self._mine_base_releases()
        return self.project

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
            if release.head in self.c2r:
                commit = commits_to_track.pop()
                commits.add(commit)
                if commit not in self.c2r:
                    self.c2r[commit] = set()
                self.c2r[commit].add(release)
            else:
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

    def _mine_base_releases(self) -> None:
        head2r = dict[Commit, Release]()
        for release in self.project.releases:
            if release.head not in head2r:
                head2r[release.head] = set[Release]()
            head2r[release.head].add(release)
        
        for release in self.project.releases:
            for tail in release.tails:
                for parent in tail.parents:
                    for base_release in self.c2r[parent]:
                        if base_release != release:
                            release.base_releases.add(base_release)
            if not release.tails:
                for base_release in self.c2r[release.head]:
                    if base_release != release:
                            release.base_releases.add(base_release)
