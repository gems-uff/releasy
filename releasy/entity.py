from builtins import property

import re

class Project():
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

    def get_issue(self, issue_id):
        if issue_id in self.__issue_map:
            return self.__issue_map[issue_id]
        else:
            return None


class Release:
    def __init__(self, tag):
        self.tag = tag
        self.base_releases = []
        self.commits = []
        self.__commit_map = {}
        self.issues = []
        self.__issue_map = {}

    @property
    def name(self):
        return self.tag.name

    def __setitem__(self, key, value):
        if isinstance(value, Commit):
            if key in self.__commit_map:
                self.commits.remove(value)
            self.__commit_map[key] = value
            self.commits.append(value)

    def add_issue(self, issue):
        if isinstance(issue, Issue):
            if issue.id in self.__issue_map:
                self.issues.remove(issue)
            self.__issue_map[issue.id] = issue
            self.issues.append(issue)

    def get_issue(self, issue_id):
        if issue_id in self.__issue_map:
            return self.__issue_map[issue_id]
        else:
            return None

    #old
    __re = re.compile(r'(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?.*')
    # Release metrics
    @property
    def size(self):
        return len(self.commits)

    @property
    def duration(self):
        return self.commits[-1].commit_time - self.commits[0].commit_time

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
    def __init__(self, hash, subject=None, parents=None, committer=None,
                 author=None, commit_time=None, author_time=None):
        self.hash = hash
        self.subject = subject
        if not parents:
            self.parents = []
        self.committer = committer
        self.commit_time = commit_time
        self.author = author
        self.author_time = author_time
        self.releases = []
        self.issues = []
        self.__issue_map = {}

    def add_issue(self, issue):
        if isinstance(issue, Issue):
            if issue.id in self.__issue_map:
                self.issues.remove(issue)
            self.issues.append(issue)
            self.__issue_map[issue.id] = issue

    def get_issue(self, issue_id):
        if issue_id in self.__issue_map:
            return self.issues.remove(issue_id)
        else:
            return None

    def __str__(self):
        return self.hash


class Issue():
    def __init__(self, id, subject=None, labels=None):
        self.id = id
        self.subject = subject
        if not labels:
            self.labels = []
        self.commits = []
        self.__commit_map = {}
        self.releases = []
        self.__release_map = {}
        self.simple_commits = []

        #old
        #todo parse
        self.labels = list()
        self.main_label = None
        self.author = None
        self.created = None
        self.closed = None
        self.released = None
        self.started = None

    def add_commit(self, commit):
        if isinstance(commit, Commit):
            if commit.hash in self.__commit_map:
                self.commits.remove(commit)
                if len(commit.parents) == 1:
                    self.simple_commits.remove(commit)
            self.commits.append(commit)
            self.__commit_map[commit.hash] = commit
            if len(commit.parents) == 1:
                self.simple_commits.append(commit)

    def get_commit(self, commit_hash):
        if commit_hash in self.__commit_map:
            return self.__commit_map[commit_hash]
        else:
            return None

    def add_release(self, release):
        if isinstance(release, Release):
            if release.name in self.__release_map:
                self.releases.remove(release)
            self.releases.append(release)
            self.__release_map[release.name] = release

    def get_release(self, release_name):
        if release_name in self.__release_map:
            return self.__release_map[release_name]
        else:
            return None

    #old
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




