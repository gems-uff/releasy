# This module connect releasy with Git

from typing import List, Set
import pygit2

from releasy.repository import Commit, Tag

class Repo:
    def tags(self):
        pass


class GitRepoAdapter:
    def __init__(self, path) -> None:
        self.path = path
        self.repo: pygit2.Repository = pygit2.Repository(path)
        self.tag_adapter = GitTagAdapter(self)
        self.commit_adapter = GitCommitAdapter(self)

    def get_tags(self) -> Set[Tag]:
        return self.tag_adapter.get_tags()

    def get_commit(self, id: str) -> Commit:
        return self.commit_adapter.get_commit(id)


class GitTagAdapter:
    def __init__(self, repo_adapter: GitRepoAdapter) -> None:
        self.repo_adapter = repo_adapter
        
    def get_tags(self) -> Set[Tag]:
        tag_refs = [ref for ref in self.repo_adapter.repo.references.objects 
                    if ref.name.startswith('refs/tags/')]

        tags: Set[Tag] = set()
        for tag_ref in tag_refs:
            tag_name = tag_ref.shorthand
            peek_commit = tag_ref.peel()
            if peek_commit.type == pygit2.GIT_OBJ_COMMIT:
                tag = Tag(tag_name, 
                        self.repo_adapter.commit_adapter.get_commit(peek_commit.hex))
                tags.add(tag)
        
        return tags


class GitCommitAdapter:
    def __init__(self, repo_adapter: GitRepoAdapter) -> None:
        self.repo = repo_adapter.repo

    def get_commit(self, commit_ref: str) -> Commit:
        commit_ref = self.repo.get(commit_ref)
        commit = Commit(commit_ref.hex, commit_ref.name)
        return commit