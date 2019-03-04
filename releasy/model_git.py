
from pygit2 import GIT_OBJ_TAG

from releasy.model import Commit, Tag


class GitTag(Tag):
    """ Encapsulate Git Tag """

    def __init__(self, repo, raw_tag):
        self.repo = repo
        self.raw_tag = raw_tag
        self.raw_commit = self.raw_tag.peel()
        self.name = self.raw_tag.shorthand
        tag_target = repo.get(raw_tag.target)
        if tag_target.type == GIT_OBJ_TAG:
            self.time = tag_target.tagger.time
            self.message = tag_target.message
        else:
            self.time = tag_target.commit_time

    @property
    def commit(self):
        return GitCommit(self.raw_commit)


class GitCommit(Commit):
    """ Encapsulate Git Commit """

    def __init__(self, qqqraw_commit):
        self.raw_commit = raw_commit
        self.children = []      #: next commits
        self.subject = None     #: first line from commit message
        self.committer = None   #: contributor responsible for the commit
        self.author = None      #: contributor responsible for the code
        self.release = None

    @property
    def id(self):
        return self.raw_commit.hex

    @property
    def parents(self):
        return [GitCommit(commit) for commit in self.raw_commit.parents]

    @property
    def message(self):
        return self.raw_commit.message