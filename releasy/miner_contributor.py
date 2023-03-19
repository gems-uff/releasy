
from typing import Any, Tuple
from releasy.miner_base import AbstractMiner
from releasy.project import Project
from releasy.contributor import ContributorSet


class ContributorMiner(AbstractMiner):
    def __init__(self) -> None:
        super().__init__()

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        previous_authors = set[str]()
        for release in sorted(
                project.releases, key = lambda r: (r.time, r.version)):

            release.contributors = ContributorSet(
                release.commits, 
                previous_authors
            )
            previous_authors.update(release.contributors.authors)
        
        return project, []
