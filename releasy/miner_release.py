from ensurepip import version
from typing import Any, Set, Tuple
import re

from .project import Project
from .release import Release, ReleaseSet
from .miner_base import AbstractMiner
from .repository import Repository

class ReleaseMiner(AbstractMiner):
    """ 
    Mine all releases 
    """
    def __init__(self) -> None:
        super().__init__()
        self.release_regexp = re.compile(
            r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
        )

    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        tags = project.repository.get_tags()

        releases: Set[Release] = set()
        for tag in tags:
            if self.release_regexp.match(tag.name):
                release = Release(project, tag.name, tag)
                releases.add(release)

        project.releases = ReleaseSet(releases)
        return (project, [])

class FinalReleaseMiner(ReleaseMiner):
    """ 
    Mine only final releases, ignoring pre releases 
    """
    def mine(self, project: Project, *args) -> Tuple[Project, Any]:
        super().mine(project, args)
        releases = ReleaseSet(release for release in project.releases 
                              if not release.version.is_pre_release())
        project.releases = releases
        return (project, [])