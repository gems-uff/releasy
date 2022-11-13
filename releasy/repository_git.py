# This module connect releasy with Git

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Set, Tuple
import pygit2

from releasy.repository import Commit, CommitSet, DiffDelta, Repository, RepositoryProxy, Tag


class GitRepository(RepositoryProxy):
    """
    A Repository proxy to Git
    """
    def __init__(self, path) -> None:
        super().__init__()
        self.path = path
        self.name = path
        self.git: pygit2.Repository = pygit2.Repository(path)
        self.commit_cache = CommitCache(self.git)
        self.repository: Repository = None

    def fetch_tags(self) -> Set[Tag]:
        rtags = [ref for ref in self.git.references.objects 
                    if ref.name.startswith('refs/tags/')]

        tags: Set[Tag] = set()
        for rtag in rtags:
            tag = self._get_tag(rtag)
            if tag:
                tags.add(tag)
        return tags

    def _get_tag(self, rtag: pygit2.Reference) -> Tag:
        ref = self.git.get(rtag.target)
        if ref.type == pygit2.GIT_OBJ_COMMIT:
            commit = self.repository.get_commit(ref.hex)
            #TODO time
            tag = Tag(self.repository, rtag.shorthand, commit)
            return tag                
        elif ref.type == pygit2.GIT_OBJ_TAG: # annotatted tag
            peel = rtag.peel()
            if peel.type == pygit2.GIT_OBJ_COMMIT:
                commit = self.repository.get_commit(rtag.peel().hex)
                rtag_ref: pygit2.Tag = ref
                try:
                    message = rtag_ref.message
                except:
                    message = ''
                if rtag_ref.tagger:
                    tagger = f"{rtag_ref.tagger.name} <{rtag_ref.tagger.email}>"
                    time_tzinfo = timezone(timedelta(minutes=rtag_ref.tagger.offset))
                    time = datetime.fromtimestamp(float(rtag_ref.tagger.time), time_tzinfo)
                    tag = Tag(self.repository, rtag.shorthand, commit, message, tagger, 
                            time)
                else:
                    tag = Tag(self.repository, rtag.shorthand, commit, message)
                return tag
        return None

    def fetch_commit(self, commit_id: str) -> Commit:
        rcommit = self.commit_cache.fetch_commit(commit_id)

        committer_tzinfo = timezone(timedelta(minutes=rcommit.committer.offset))
        committer_time = datetime.fromtimestamp(float(rcommit.committer.time), committer_tzinfo)
        author_tzinfo = timezone(timedelta(minutes=rcommit.author.offset))
        author_time = datetime.fromtimestamp(float(rcommit.author.time), author_tzinfo)

        try:
            message = rcommit.name,
        except:
            message = ''

        commit = Commit(
            self.repository,
            rcommit.hex,
            message,
            f"{rcommit.committer.name} <{rcommit.committer.email}>",
            committer_time,
            f"{rcommit.author.name} <{rcommit.author.email}>",
            author_time)
        return commit

    def fetch_commit_parents(self, commit: Commit) -> CommitSet:
        commit_ref: pygit2.Commit = self.commit_cache.fetch_commit(commit.id)
        parents = CommitSet()
        for parent_ref in commit_ref.parents:
            parent = self.repository.get_commit(parent_ref.hex)
            parents.add(parent)
        return parents

    def diff(self, commit_a: Commit, commit_b: Commit, parse_delta:bool = False) -> DiffDelta:
        diff_result = self.git.diff(commit_a.id, commit_b.id)

        files = set()
        if parse_delta:
            for delta in diff_result.deltas:
                if delta.new_file.path:
                    files.add(delta.new_file.path)
                if delta.old_file.path:
                    files.add(delta.old_file.path)

        delta = DiffDelta(
            diff_result.stats.insertions, 
            diff_result.stats.deletions,
            diff_result.stats.files_changed,
            files)
        return delta

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
