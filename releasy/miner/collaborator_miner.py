from typing import Dict
from .factory import AbstractMiner
from ..project import Project


class NewcomerMiner(AbstractMiner):
    """ Mine newcomers, that is new collaborattors to the project """
    def mine(self, project: Project, params: Dict[str, object]) -> Project:
        collaborattors = set()
        for release in project.releases:
            release.newcomers = set()
            for commit in release.commits:
                if commit.committer not in collaborattors:
                    release.newcomers.add(commit.committer)
                if commit.author not in collaborattors:
                    release.newcomers.add(commit.author)
                collaborattors.add(commit.committer)
                collaborattors.add(commit.author)
        return project
