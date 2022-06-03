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
            self._mine_base_releases()
        return self.project

    def _mine_base_releases(self):
        for release in self.project.releases:
            for tail in release.tails:
                for parent in tail.parents:
                    pass
        return self.project
