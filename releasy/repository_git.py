# This module connect releasy with Git

from typing import Dict, List, Set
import pygit2

from releasy.repository import Commit, RepositoryProxy, Tag


class GitRepository(RepositoryProxy):
    """
    A Repository proxy to Git
    """
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
        self.git: pygit2.Repository = pygit2.Repository(path)
        self.commit_cache = CommitCache(self.git)

    def fetch_tags(self) -> Set[Tag]:
        tag_refs = [ref for ref in self.git.references.objects 
                    if ref.name.startswith('refs/tags/')]

        tags: Set[Tag] = set()
        for tag_ref in tag_refs:
            tag_name = tag_ref.shorthand
            peek = tag_ref.peel()
            if peek.type == pygit2.GIT_OBJ_COMMIT:
                tag = Tag(None, tag_name, self.fetch_commit(peek.hex))
                tags.add(tag)
        
        return tags

    def fetch_commit(self, commit_id: str) -> Commit:
        commit_ref = self.commit_cache.fetch_commit(commit_id)
        commit = Commit(None, commit_ref.hex, commit_ref.name)
        return commit

    def fetch_commit_parents(self, commit: Commit) -> Set[Commit]:
        commit_ref: pygit2.Commit = self.git.get(commit.id)
        parents: Set[Commit] = set()
        for parent_ref in commit_ref.parents:
            parent = self.fetch_commit(parent_ref.hex)
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
