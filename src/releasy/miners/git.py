from typing import List
import pygit2
from datetime import datetime

from releasy.models.release import Release, ReleaseList
from releasy.models.commit import Commit, CommitList
from releasy.models.contributor import Contributor


class GitMiner():
    """Mines releases from the tags of a Git repository."""
    def __init__(self, repository_path=None):
        if not repository_path:
            raise ValueError("Repository path must be provided")
        self.repository_path = repository_path
        self.commits = CommitList()  # Will hold CommitList, indexed by id


    def mine_releases(self) -> ReleaseList:
        """Mine the releases"""
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

            head = self._commit_from_git_commit(head)
            release = Release(
                name=release_name,
                timestamp=timestamp,
                author=author,
                head=head,
                message=message
            )
            releases.append(release)

        return releases

    def mine_commits(self) -> CommitList:
        """Mine the commits"""
        repository = pygit2.Repository(self.repository_path)
        commits = CommitList()
        git_commits: List[pygit2.Commit] = []

        for git_commit in repository.walk(repository.head.target):
            commit = self._commit_from_git_commit(git_commit)
            commits.append(commit)
            git_commits.append(git_commit)

        # Link parent commits by reusing created commit objects
        for git_commit in git_commits:
            commit = commits[str(git_commit.id)]
            for parent_id in git_commit.parent_ids:
                commit.parents.append(commits[str(parent_id)])

        return CommitList(commits)

    def _commit_from_git_commit(self, git_commit) -> Commit:
        author = Contributor(
            name=git_commit.author.name,
            email=git_commit.author.email
        )
        committer = Contributor(
            name=git_commit.committer.name,
            email=git_commit.committer.email
        )
        author_time = datetime.fromtimestamp(git_commit.author.time)
        committer_time = datetime.fromtimestamp(git_commit.committer.time)
        return Commit(
            id=str(git_commit.id),
            message=git_commit.message,
            committer=committer,
            committer_time=committer_time,
            author=author,
            author_time=author_time
        )
