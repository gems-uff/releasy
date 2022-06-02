from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Generic, Set, TypeVar
if TYPE_CHECKING:
    from releasy.release import Release
    from releasy.semantic import SemanticRelease


T = TypeVar('T')
class ReleaseSet(Generic[T]):
    def __init__(self, releases: Set[T] = None) -> None:
        self._releases: Dict[str, Set] = {}
        if releases:
            for release in releases:
                self.add(release)

    def __iter__(self):
        return (release for release in self._releases.values())

    def __getitem__(self, key) -> T:
        if isinstance(key, int):
            release_name = list(self._releases.keys())[key]
            return self._releases[release_name]
        elif isinstance(key, str):
            return self._releases[key]
        else:
            raise TypeError()

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            if item in self._releases:
                return True
        return False

    def add(self, release: T):
        if release:
            self._releases[release.name] = release

    def update(self, iterable):
        for item in iterable:
            self.add(item)

    def __len__(self):
        return len(self._releases)


