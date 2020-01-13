from typing import List, Dict
from datetime import datetime, timezone, timedelta

import pygit2
# from pygit2 import Repository, Reference, GIT_OBJ_TAG

from releasy.model import Project, Tag, Commit, CommitStats
from ...developer import Developer
from .miner import Vcs

class GitVcs(Vcs):
    """ Encapsulate Git Version Control System using pygit2 lib """

    def __init__(self, path: str):
        super().__init__(path)
        self._repo: pygit2.Repository = pygit2.Repository(path)
        self._tag_cache: Dict[Tag] = {}
        self._commit_cache: Dict[Commit] = {}

    def tags(self) -> List[Tag]:
        repo = self._repo
        refs = (ref for ref in repo.references.objects if ref.name.startswith('refs/tags/'))
        tags = [self.get_tag(ref) for ref in refs]
        return tags

    def get_tag(self, rtag: pygit2.Reference) -> Tag:
        """ Tag factory """
        tagname = rtag.shorthand
        if tagname not in self._tag_cache:
            tag = GitTag(self, rtag)
            self._tag_cache[tagname] = tag
        return self._tag_cache[tagname]

    def get_commit(self, raw_commit: pygit2.Commit) -> Commit:
        """ Commit factory """
        hashcode = raw_commit.hex
        if hashcode not in self._commit_cache:
            commit = GitCommit(self, raw_commit)
            self._commit_cache[hashcode] = commit
        return self._commit_cache[hashcode]


class GitTag(Tag):
    """ Encapsulate Git Tag """

    def __init__(self, vcs: GitVcs, rtag: pygit2.Reference):
        name = rtag.shorthand
        commit = None
        time = None
        message = None
        raw_commit = rtag.peel()
        if raw_commit.type == pygit2.GIT_OBJ_COMMIT:
            commit = vcs.get_commit(raw_commit)

            target = vcs._repo.get(rtag.target) 
            if target.type == pygit2.GIT_OBJ_TAG: # Annotated commit
                if target.tagger:
                    tagger_tzinfo = timezone(timedelta(minutes=target.tagger.offset))
                    time = datetime.fromtimestamp(float(target.tagger.time), tagger_tzinfo)
                try:
                    message = target.message
                except:
                    message = ""
        
        super().__init__(name=name, commit=commit, time=time, message=message)


class GitCommit(Commit):
    """ Encapsulate Git Commit """

    def __init__(self, vcs: GitVcs, raw_commit: pygit2.Commit):
        self._vcs = vcs
        self._raw_commit = raw_commit

        author = Developer(login=raw_commit.author.email, email=raw_commit.author.email, name=raw_commit.author.name)
        author_tzinfo = timezone(timedelta(minutes=raw_commit.author.offset))
        author_time = datetime.fromtimestamp(float(raw_commit.author.time), author_tzinfo)

        committer = Developer(login=raw_commit.committer.email, email=raw_commit.committer.email, name=raw_commit.committer.name)
        committer_tzinfo = timezone(timedelta(minutes=raw_commit.committer.offset))
        committer_time = datetime.fromtimestamp(float(raw_commit.committer.time), committer_tzinfo)

        try: #TODO fix problem with encodes
            message = raw_commit.message
        except:
            message = ""

        super().__init__(
            hashcode=raw_commit.hex,
            #parents=[],
            message=message,
            author=author,
            author_time=author_time,
            committer=committer,
            committer_time=committer_time
        )
        
    @property
    def parents(self):
        # late bind method to avoid high memory usage
        return [self._vcs.get_commit(rparent) for rparent in self._raw_commit.parents]

    @parents.setter
    def parents(self, parents):
        pass

    @property
    def stats(self) -> CommitStats:
        if not self._stats:
            self._stats = CommitStats()
            if self.__raw.parents:
                for raw_parent in self.__raw.parents:
                    diff = self.__raw.tree.diff_to_tree(raw_parent.tree)
                    self._stats += diff.stats
            else:
                diff = self.__raw.tree.diff_to_tree()
                self._stats += diff.stats
        return self._stats

    #todo this method is not in the best place
    #     consider change it to some util class
    def diff_stats(self, commit=None):
        """ Calculate diff stats from another commit. This method is useful to
        calculate release churn """

        stats = CommitStats()
        if commit:
            diff = self.__raw.tree.diff_to_tree(commit.__raw.tree)
        else:
            diff = self.__raw.tree.diff_to_tree()
        # intentionaly inverted
        stats.insertions = diff.stats.deletions
        stats.deletions = diff.stats.insertions
        stats.files_changed = diff.stats.files_changed
        return stats






