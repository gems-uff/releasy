import pygit2
from datetime import datetime
from releasy.models.release import Release, ReleaseList
from releasy.models.version import ReleaseVersion
from releasy.models.contributor import Contributor
from releasy.models.commit import Commit


class GitReleaseMiner():
    """Mines releases from the tags of a Git repository."""
    def __init__(self, repository_path=None):
        self.repository_path = repository_path

    def mine(self) -> ReleaseList:
        """Mine the releases"""
        if not self.repository_path:
            raise ValueError("Repository path must be provided")
            
        repository = pygit2.Repository(self.repository_path)
        releases = ReleaseList()

        tag_references = (
            reference
            for reference in repository.references
            if reference.startswith('refs/tags/')
        )

        for tag_reference in tag_references:
            release_name = tag_reference.replace('refs/tags/', '')
            tag = repository.get(
                repository.references.get(tag_reference).target
            )

            if tag.type == pygit2.GIT_OBJECT_TAG:
                head_reference = tag.target
                head = repository.get(head_reference)
                if head.type != pygit2.GIT_OBJECT_COMMIT:
                    continue
                author = Contributor(
                    name=tag.tagger.name,
                    email=tag.tagger.email
                )
                timestamp = datetime.fromtimestamp(tag.tagger.time)
                message = tag.message if tag.message else None
            
            elif tag.type == pygit2.GIT_OBJECT_COMMIT:
                head = tag
                author = Contributor(
                    name=head.committer.name,
                    email=head.committer.email
                )
                timestamp = datetime.fromtimestamp(head.committer.time)
                message = head.message if head.message else None

            release = Release(
                name=release_name,
                timestamp=timestamp,
                author=author,
                head=head.id,
                message=message
            )
            releases.append(release)

        return releases
