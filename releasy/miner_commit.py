"""Commit Miner

This module mine commits and assign them to releases.

For each release, it assigns:
- its commits: the commits that belong to the release; and
- its tail commits: the first commits of each release branch
"""

from typing import List

from releasy.commit import Commit
from .miner_main import AbstractMiner
from .release import Project


class HistoryCommitMiner(AbstractMiner):
    def mine(self) -> Project:
        release_commits = set(map(lambda release: release.tag.commit, 
                              self.project.releases))

        for release in self.project.releases:
            commits = set()
            tails = set()
            loop_detector = set()
            commits_to_track: List[Commit] = [release.tag.commit]
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
        return self.project
