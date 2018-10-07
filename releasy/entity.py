
class Developer(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return "%s <%s>" % (self.name, self.email)

class Tag(object):
    def __init__(self, name, commit=None):
        self.name = name
        self.commit = commit

    def __str__(self):
        return "%s" % self.name

class Commit(object):
    def __init__(self, hash, subject=None, parent=None, commiter=None, developer=None, commit_time=None, development_time=None):
        self.hash = hash
        self.subject = subject
        self.parent = parent
        self.developer = developer
        self.commiter = commiter
        self.commit_time = commit_time
        self.development_time = development_time
        self.tag = []
        self.release = []
        self.issue = []

    def __str__(self):
        return self.hash

class Issue():
    def __init__(self, id, subject=None):
        self.id = id
        self.subject = subject
        # --- #
        self.labels = list()
        self.main_label = None
        self.commits = list()
        self.author = None
        self.created = None
        self.closed = None
        self.released = None
        self.started = None

    def __str__(self):
        return "%i" % self.id

class CommitGroup(object):
    def __init__(self):
        self.commit = {}
        self.issue = {}

    def get_commit(self):
        return self.commit

class Release(CommitGroup):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag
#        self.name = tag.name
#        self.commits = list()
#        self.issues = list()
#        self.duration = 0
#        self.authors = list()
#        self.commiters = list()
#        self.direct_commits = list()
#        self.previous = list()

    def __str__(self):
        return "%s" % self.tag.name

class Project(object):
    def __init__(self):
        self.release = {'ALL': CommitGroup()}
        self.developer = {}
        self.tag = {}
