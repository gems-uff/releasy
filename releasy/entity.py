
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
    def __init__(self, hash, subject=None, parent=None, commiter=None,
                 developer=None, commit_time=None, development_time=None):
        self.hash = hash
        self.subject = subject
        self.parent = parent
        self.commiter = commiter
        self.commit_time = commit_time
        self.developer = developer
        self.development_time = development_time
        self.issues = []

        #todo remove:
        self.release = []

    def __str__(self):
        return self.hash

class Issue():
    def __init__(self, id, subject=None):
        self.id = id
        self.__subject = subject

        #todo parse
        self.labels = list()
        self.main_label = None
        self.commits = list()
        self.author = None
        self.created = None
        self.closed = None
        self.released = None
        self.started = None

    @property
    def subject(self):
        if self.__subject:
            return self.__subject
        else:
            return ""

    def __str__(self):
        return "%i" % self.id


class Release:
    def __init__(self, tag):
        super().__init__()
        self.__tag = tag
        self.__commits = {}
        self.__base_releases = []

    @property
    def name(self):
        return self.__tag.name

    @property
    def tag(self):
        return self.__tag

    @property
    def time(self):
        return self.tag.commit.commit_time

    @property
    def commits(self):
        ''' return all commits of the release '''
        return self.__commits.values()

    def add_commit(self, commit):
        if commit.hash not in self.__commits.keys():
            self.__commits[commit.hash] = commit

    @property
    def developers(self):
        ''' return all developers of the release '''
        developers = {}
        for commit in self.__commits.values():
            developers[commit.developer.email] = commit.developer
        return developers.values()

    @property
    def issues(self):
        ''' return all issues of the release '''
        issues = {}
        for commit in self.__commits.values():
            for issue in commit.issues:
                issues[issue.id] = issue
        return issues.values()

    @property
    def base_releases(self):
        return self.__base_releases

    def add_base_release(self, release):
        self.__base_releases.append(release)

    def __str__(self):
        return "%s" % self.tag.name

class Project(object):
    def __init__(self):
        self.__releases = {}

    @property
    def releases(self):
        return self.__releases.values()

    def release(self, ref):
        return self.__releases[ref]

    def add_release(self, release):
        self.__releases[release.name] = release

    def contains_release(self, ref):
        return ref in self.__releases.keys()
