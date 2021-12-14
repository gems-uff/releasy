from typing import Dict
from releasy.miner import AbstractMiner
from releasy.release import ReleaseSet


class NewcomerMiner(AbstractMiner):
    """ Mine newcomers, that is new collaborattors to the project """
    def mine(self, releases: ReleaseSet, params: Dict[str, object]) -> ReleaseSet:
        collaborattors = set()
        for release in releases:
            release.newcomers = set()
            for commit in release.commits:
                if commit.committer not in collaborattors:
                    release.newcomers.add(commit.committer)
                if commit.author not in collaborattors:
                    release.newcomers.add(commit.author)
                collaborattors.add(commit.committer)
                collaborattors.add(commit.author)
        return releases
