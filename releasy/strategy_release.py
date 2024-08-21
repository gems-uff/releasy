


from typing import Set
from releasy.old.version_format import ReleaseVersionFormat
from releasy.release import Release
from releasy.repository import Repository


class ReferenceReleaseStrategy:
    def __init__(self, version_format: ReleaseVersionFormat) -> None:
        self.version_format = version_format

    def assign(self, repository: Repository, releases: Set[Release] = None) -> Set[Release]:
        releases = list[Release]()

        for (name, head, author, timestamp) in repository.release_refs():
            version = self.version_format.parse(name)
            if not version:
                continue

            release = Release(version, timestamp, None, author)
            releases.append(release)

        return releases

    
    