from builtins import property

import re

class Project(object):
    def __init__(self, config):
        self.config = config
        self.releases = []
        self.__release_map = {}
        self.issues = []
        self.__issue_map = {}


    def __setitem__(self, key, value):
        if isinstance(value, Release):
            if key in self.__release_map:
                return self.releases.remove(value)
            self.__release_map[key] = value
            self.releases.append(value)

    def add_issue(self, issue):
        if isinstance(issue, Issue):
            if issue.id in self.__issue_map:
                return self.issues.remove(issue)
            self.__issue_map[issue.id] = issue
            self.issues.append(issue)


class Release:
    def __init__(self, tag):
        self.tag = tag
        self.base_releases = []
        self.commits = []
        self.__commit_map = {}

    #old
        self.__first_commit = None
        self.__last_commit = None

    @property
    def name(self):
        return self.tag.name

    def __setitem__(self, key, value):
        if isinstance(value, Commit):
            if key in self.__commit_map:
                self.commits.remove(value)
            self.__commit_map[key] = value
            self.commits.append(value)

    #old

    __re = re.compile(r'(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?.*')
    # Release metrics
    @property
    def size(self):
        return len(self.commits)

    @property
    def duration(self):
        return self.__last_commit.commit_time - self.__first_commit.commit_time

    @property
    def number_of_contributors(self):
        contributors = {}
        for commit in self.commits:
            contributors[commit.commiter] = 1
        return len(contributors.keys())

    @property
    def number_of_merges(self):
        merges = 0
        for commit in self.commits:
            if len(commit.parent) > 1:
                merges += 1
        return merges

    @property
    def bugfix_effort(self):
        bugfix = 0
#        for issue in self.issues:


    # End of release metrics



    @property
    def time(self):
        return self.tag.time

    @property
    def time(self):
        return self.tag.commit.commit_time

    @property
    def first_commit(self):
        return self.__first_commit

    @property
    def last_commit(self):
        return self.__last_commit

    @property
    def type(self):
        current = Release.__re.match(self.name)
        if current:
            if current.group('patch') != '0':
                return 'PATCH'
            elif current.group('minor') != '0':
                return 'MINOR'
            else:
                return 'MAJOR'
        else:
            return 'UNKNOWN'

    def add_commit(self, commit):
        if commit.hash not in self.__commits.keys():
            self.__commits[commit.hash] = commit
            if not self.__first_commit or commit.commit_time < self.__first_commit.commit_time:
                self.__first_commit = commit
            if not self.__last_commit or commit.commit_time > self.__last_commit.commit_time:
                self.__last_commit = commit

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

    def __str__(self):
        return "%s" % self.tag.name

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
        #old
        self.release = None

    @property
    def time(self):
        return self.commit.commit_time

    def is_release(self):
        return True

    def __str__(self):
        return "%s" % self.name

class Commit(object):
    def __init__(self, hash, subject=None, parents=[], committer=None,
                 author=None, commit_time=None, author_time=None):
        self.hash = hash
        self.subject = subject
        self.parents = parents
        self.committer = committer
        self.commit_time = commit_time
        self.author = author
        self.author_time = author_time
        self.releases = []
    # old
        self.issues = []

    def __str__(self):
        return self.hash


class Issue():
    def __init__(self, id, subject=None, labels=[]):
        self.id = id
        self.subject = subject
        self.labels = labels

        #old
        self.commits = []

        #todo parse
        self.labels = list()
        self.main_label = None
        self.author = None
        self.created = None
        self.closed = None
        self.released = None
        self.started = None

    @property
    def first_commit(self):
        return self.commits[0]

    @property
    def last_commit(self):
        return self.commits[-1]

    @property
    def duration(self):
        return self.last_commit.commit_time - self.first_commit.commit_time

    def __str__(self):
        return "%i" % self.id




