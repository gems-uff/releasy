
class Developer(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return "%s <%s>" % (self.name, self.email)

class Tag(object):
    def __init__(self, ref, commit=None):
        self.ref = ref
        self.commit = commit

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

    def __str__(self):
        return self.hash

class CommitGroup(object):
    def __init__(self):
        self.commit = {}

    def get_commit(self):
        return self.commit

class Release(CommitGroup):
    def __init__(self, tag):
        self.tag = tag
#        self.name = tag.name
#        self.commits = list()
#        self.issues = list()
#        self.duration = 0
#        self.authors = list()
#        self.commiters = list()
#        self.direct_commits = list()
#        self.previous = list()

class Project(object):
    def __init__(self):
        self.release = {'ALL': CommitGroup()}
        self.developer = {}
        self.tag = {}
