# This module connect releasy with Git

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Set
import pygit2

from releasy.repository import Commit, CommitSet, Repository, RepositoryProxy, Tag


class GitRepository(RepositoryProxy):
    """
    A Repository proxy to Git
    """
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
        self.git: pygit2.Repository = pygit2.Repository(path)
        self.commit_cache = CommitCache(self.git)
        self.repository: Repository = None

    def fetch_tags(self) -> Set[Tag]:
        tag_refs = [ref for ref in self.git.references.objects 
                    if ref.name.startswith('refs/tags/')]

        tags: Set[Tag] = set()
        for tag_ref in tag_refs:
            tag_name = tag_ref.shorthand
            peek = tag_ref.peel()
            if peek.type == pygit2.GIT_OBJ_COMMIT:
                tag = Tag(self.repository, tag_name, self.repository.get_commit(peek.hex))
                tags.add(tag)
        return tags

    def fetch_commit(self, commit_id: str) -> Commit:
        commit_ref = self.commit_cache.fetch_commit(commit_id)

        committer_tzinfo = timezone(timedelta(minutes=commit_ref.committer.offset))
        committer_time = datetime.fromtimestamp(float(commit_ref.committer.time), committer_tzinfo)
        author_tzinfo = timezone(timedelta(minutes=commit_ref.author.offset))
        author_time = datetime.fromtimestamp(float(commit_ref.author.time), author_tzinfo)

        commit = Commit(
            self.repository,
            commit_ref.hex,
            commit_ref.name,
            f"{commit_ref.committer.name} <{commit_ref.committer.email}>",
            committer_time,
            f"{commit_ref.author.name} <{commit_ref.author.email}>",
            author_time)
        return commit

    def fetch_commit_parents(self, commit: Commit) -> CommitSet:
        commit_ref: pygit2.Commit = self.commit_cache.fetch_commit(commit.id)
        parents = CommitSet()
        for parent_ref in commit_ref.parents:
            parent = self.repository.get_commit(parent_ref.hex)
            parents.add(parent)
        return parents


class CommitCache:
    """
    Implement a cache to improve fech commit performance
    """
    def __init__(self, git: pygit2.Repository) -> None:
        self.git =  git
        self.cache: Dict[str, pygit2.Commit] = {}

    def fetch_commit(self, commit_id: str) -> pygit2.Commit:
        if commit_id not in self.cache:
            commit_ref: pygit2.Commit = self.git.get(commit_id)
            self.cache[commit_id] = commit_ref
        return self.cache[commit_id]
