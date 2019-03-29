
from datetime import datetime, timezone, timedelta
from pygit2 import Repository
from pygit2 import GIT_OBJ_TAG

from releasy.model import Project, Vcs, Tag, Commit, CommitStats


class GitVcs(Vcs):
    """ Encapsulate Git Version Control System using pygit2 lib

    Attributes:
        repository: git repository
    """

    def __init__(self):
        super().__init__()
        self.repository = None

    def path(self, path):
        self.repository = Repository(path)
    path = property(fset=path)

    @property
    def tagnames(self):
        return [ref[10:] for ref in self.repository.references if ref.startswith('refs/tags/')]

    def load_tag(self, tagname):
        if tagname not in self._tag_cache:
            raw_tag = self.repository.lookup_reference("refs/tags/%s" % tagname)
            self._tag_cache[tagname] = GitTag(self, raw_tag)
        return self._tag_cache[tagname]

    def load_commit(self, id, raw_commit=None):
        if id not in self._commit_cache:
            if not raw_commit:
                raw_commit = None #TODO fetch

            committer_email = raw_commit.committer.email
            committer_name = raw_commit.committer.name
            committer = self.developer_db.load_developer(name=committer_name, email=committer_email)

            author_email = raw_commit.author.email
            author_name = raw_commit.author.name
            author = self.developer_db.load_developer(name=author_name, email=author_email)

            commit = GitCommit(self, raw_commit)
            commit.committer = committer
            commit.author = author
            self._commit_cache[id] = commit

        return self._commit_cache[id]


class GitTag(Tag):
    """ Encapsulate Git Tag """

    def __init__(self, vcs, raw_tag):
        super().__init__()
        self.__vcs = vcs
        self.__raw = raw_tag
        self.name = self.__raw.shorthand
        self.message = None
        raw_commit = self.__raw.peel()
        self.commit = self.__vcs.load_commit(raw_commit.hex, raw_commit)
        target = self.__vcs.repository.get(self.__raw.target)
        if target.type == GIT_OBJ_TAG:
            tagger_tzinfo = timezone(timedelta(minutes=target.tagger.offset))
            self.time = datetime.fromtimestamp(float(target.tagger.time), tagger_tzinfo)
            try:
                self.message = target.message
            except:
                self.message = ''
        else:
            self.time = self.commit.time


class GitCommit(Commit):
    """ Encapsulate Git Commit """

    def __init__(self, vcs, raw_commit):
        super().__init__()
        self.__vcs = vcs
        self.__raw = raw_commit
        self.id = self.__raw.hex
        try: #TODO fix problem with encodes
            self.message = self.__raw.message
            self.subject = self.message.split('\n', 1)[0]
        except:
            self.message = ''
            self.subject = ''
        self.release = None

        # author = self.developer_factory.create(raw_commit.author)
        author_tzinfo = timezone(timedelta(minutes=self.__raw.author.offset))
        self.author_time = datetime.fromtimestamp(float(raw_commit.author.time), author_tzinfo)

        # committer = self.developer_factory.create(raw_commit.committer)
        committer_tzinfo = timezone(timedelta(minutes=raw_commit.committer.offset))
        self.time = datetime.fromtimestamp(float(raw_commit.committer.time), committer_tzinfo)

    @property
    def parents(self):
        # late bind method to avoid memory leak
        return [self.__vcs.load_commit(commit.hex, commit) for commit in self.__raw.parents]

    @property
    def stats(self) -> CommitStats:
        if not self._stats:
            self._stats = CommitStats()
            if self.parents:
                for parent in self.parents:
                    diff = self.__vcs.repository.diff(parent._GitCommit__raw, self.__raw)
                    self._stats.insertions += diff.stats.insertions
                    self._stats.deletions += diff.stats.deletions
                    self._stats.files_changed += diff.stats.files_changed
        return self._stats




