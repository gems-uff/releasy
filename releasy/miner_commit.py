from typing import List

from releasy.commit import Commit
from .miner_main import AbstractMiner, Project

class HistoryCommitMiner(AbstractMiner):
    def mine(self) -> Project:
        # commits = self.project.repository.get_commits()
        release_commits = set(map(lambda release: release.tag.commit, 
                              self.project.releases))

        for release in self.project.releases:
            commits = set()
            commits_to_track: List[Commit] = [release.tag.commit]
            while commits_to_track:
                commit = commits_to_track.pop()
                commits.add(commit)

                for parent in commit.parents:
                    if parent not in release_commits:
                        commits_to_track.append(parent)
            
            release.commits = commits

        # for commit in commits:
        #     release_commits = commit.history_until(release_commits)
        return self.project
