from typing import Set
import re

from .miner_main import AbstractMiner, Project, Release, ReleaseSet
from .repository import Repository

class ReleaseMiner(AbstractMiner):
    def __init__(self, project: Project) -> None:
        super().__init__(project)
        self.release_regexp = re.compile(
            r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
        )

    def mine(self) -> Project:
        project = self.project
        tags = self.project.repository.get_tags()

        releases: Set[Release] = set()
        for tag in tags:
            if self.release_regexp.match(tag.name):
                release = Release(self.project, tag.name, tag)
                releases.add(release)

        project.release = ReleaseSet(releases)
        return project