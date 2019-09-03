from typing import List, Dict
from datetime import datetime, timezone, timedelta

import pygit2
# from pygit2 import Repository, Reference, GIT_OBJ_TAG

from releasy.model import Project, Tag, Commit, CommitStats
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

    def get_commit(self, rcommit: pygit2.Commit) -> Commit:
        """ Commit factory """
        hashcode = rcommit.hex
        if hashcode not in self._commit_cache:
            commit = GitCommit(self, rcommit)
            self._commit_cache[hashcode] = commit
        return self._commit_cache[hashcode]


class GitTag(Tag):
    """ Encapsulate Git Tag """

    def __init__(self, vcs: GitVcs, rtag: pygit2.Reference):
        name = rtag.shorthand
        rcommit = rtag.peel()
        commit = vcs.get_commit(rcommit)
        target = vcs._repo.get(rtag.target)
        if target.type == pygit2.GIT_OBJ_TAG:
            tagger_tzinfo = timezone(timedelta(minutes=target.tagger.offset))
            time = datetime.fromtimestamp(float(target.tagger.time), tagger_tzinfo)
            try:
                message = target.message
            except:
                message = ""
        else:
            time = commit.committer_time
            message = commit.committer_time
        super().__init__(name=name, commit=commit, time=time, message=message)


class GitCommit(Commit):
    """ Encapsulate Git Commit """

    def __init__(self, vcs: GitVcs, rcommit: pygit2.Commit):
        self._vcs = vcs
        self._rcommit = rcommit

        author = None #self.developer_factory.create(rcommit.author)
        author_tzinfo = timezone(timedelta(minutes=rcommit.author.offset))
        author_time = datetime.fromtimestamp(float(rcommit.author.time), author_tzinfo)

        committer = None #self.developer_factory.create(rcommit.committer)
        committer_tzinfo = timezone(timedelta(minutes=rcommit.committer.offset))
        committer_time = datetime.fromtimestamp(float(rcommit.committer.time), committer_tzinfo)

        try: #TODO fix problem with encodes
            message = rcommit.message
        except:
            message = ""

        super().__init__(
            hashcode=rcommit.hex,
            #parents=[],
            message=message,
            #author=None,
            author_time=author_time,
            #committer=None,
            committer_time=committer_time
        )
        
    @property
    def parents(self):
        # late bind method to avoid high memory usage
        return [self._vcs.get_commit(rparent) for rparent in self._rcommit.parents]

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






