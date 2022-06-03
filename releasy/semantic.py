from __future__ import annotations
from typing import Dict, Generic, Set, TypeVar
from .release import Project, Release
from .repository import Commit
from .collection import ReleaseSet



class SemanticRelease:
    def __init__(self, project: Project, name: str, releases: Set[Release]):
        self.project = project
        self.name = name
        self.releases = releases
        self.commits: Set[Commit]= set()
    
    def __hash__(self):
        return hash((self.project, self.name))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, SemanticRelease):
            return self.project == __o.project and self.name == __o.name
        else:
            return False

    def __repr__(self) -> str:
        return self.name


class FinalRelease(SemanticRelease):
    pass

#TODO implement pre release logic
class PreRelease(SemanticRelease):
    pass


class MainRelease(FinalRelease):
    def __init__(self, project: Project, name: str, releases: ReleaseSet[Release],
                 patches: Set[Release]) -> None:
        super().__init__(project, name, releases)
        self.patches = ReleaseSet(patches)


class Patch(FinalRelease):
    def __init__(self, project: Project, name: str, releases: ReleaseSet[Release]) -> None:
        super().__init__(project, name, releases)   


SR = TypeVar('SR')
class SReleaseSet(Generic[SR]):
    def __init__(self, sreleases: Set[SR] = None) -> None:
        self._sreleases: Dict[str, SR] = dict()
        if sreleases:
            for srelease in sreleases:
                self.add(srelease)

    def __len__(self):
        return len(self._sreleases)

    def __contains__(self, item) -> bool:
        if isinstance(item, str) and item in self._sreleases:
            return True
        elif isinstance(item, SemanticRelease) and item.name in self._sreleases:
            return True
        else:
            return False

    def __getitem__(self, key) -> SR:
        if isinstance(key, int):
            release_name = list(self._sreleases.keys())[key]
            return self._sreleases[release_name]
        elif isinstance(key, str):
            return self._sreleases[key]
        else:
            raise TypeError()

    def add(self, srelease: SR):
        if srelease and srelease.name not in self._sreleases:
            self._sreleases[srelease.name] = srelease

    def merge(self, srelease: SR):
        if srelease in self:
            name = srelease.name
            stored_srelease = self[name]

            for release in srelease.releases:
                if release not in stored_srelease.releases:
                    stored_srelease.releases.add(release)
        else:
            self.add(srelease)