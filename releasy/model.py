"""
Releasy Meta Model
"""

import re


class Project:
    """
    Software Project

    Attributes:
        releases: list of project releases, sorted by date
        release_pattern: compiled regexp to match if a tag is a release
        vcs: version control system
        tagnames (readonly): list of tag names
    """

    def __init__(self, name, path, regexp=None):
        self.name = name
        self.path = path
        self.releases = []  #: list of project releases
                            #: regexp to match release name
        self.__vcs = None
        self.__developer_db = None
        self.authors = []

        if regexp:
            self.release_pattern = re.compile(regexp)
        else:
            self.release_pattern = re.compile(r'(v|r|maven-|go|rel-|release(/|-)|mongodb-)?(?P<major>[0-9]+)(\.(?P<minor>[0-9]+))?(\.(?P<patch>[0-9]+))?.*')

    @property
    def vcs(self):
        return self.__vcs

    @vcs.setter
    def vcs(self, vcs):
        self.__vcs = vcs
        self.__vcs.path = self.path
        if self.__developer_db:
            self.__vcs.developer_db = self.developer_db

    @property
    def developer_db(self):
        return self.__developer_db

    @developer_db.setter
    def developer_db(self, developer_db):
        self.__developer_db = developer_db
        if self.__vcs:
            self.__vcs.developer_db = developer_db

    @property
    def tagnames(self):
        return self.vcs.tagnames

    def load(self):
        """ load project data """
        self.__load_releases()
        self.__load_commits()

    def __load_releases(self):
        """ Load release data """
        for tagname in self.tagnames:
            if self.is_release_tag(tagname):
                tag = self.vcs.load_tag(tagname)
                self.releases.append(Release(self, tag))
        self.releases = sorted(self.releases, key=lambda release: release.time)

    def __load_commits(self):
        for release in self.releases:
            track_release(self, release)

    def is_release_tag(self, tagname):
        return is_release_tag(self, tagname)


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """

    def __init__(self):
        self._commit_cache = {}
        self._tag_cache = {}
        self.developer_db = None

    def load_tag(self):
        """ load tag from version control """
        pass

    def load_commit(self):
        """ load commit from version control """
        pass


class Release:
    """
    Software Release

    Attributes:
        name (str): release name
        description (str): release description
        time: release creation time
        commits: list of commits that belong exclusively to this release
        merges: list of merge commits that belong exclusively to this release
        tag: tag that represents the release
        head: commit referred  by release.tag
        tails: list of commits where the release begin
        developers: list of authors and committers
        committers: list of committers
        authors: list of authors
    """

    def __init__(self, project, tag):
        self.project = project
        self.tag = tag
        self.commits = []
        self.merges = []
        self.tails = []
        self.developers = []
        self.committers = []
        self.authors = []
        self.newcommers = []

    @property
    def name(self):
        return self.tag.name

    @property
    def description(self):
        return self.tag.message

    @property
    def time(self):
        return self.tag.time

    @property
    def head(self):
        return self.tag.commit

    @property
    def commit_count(self):
        return len(self.commits)

    @property
    def merge_count(self):
        return len(self.merges)

    @property
    def developer_count(self):
        return len(self.developers)

    @property
    def newcommer_count(self):
        return len(self.newcommers)

    @property
    def typename(self):
        current = self.project.release_pattern.match(self.name)
        if current:
            if current.group('patch') != '0':
                return 'PATCH'
            elif current.group('minor') != '0':
                return 'MINOR'
            else:
                return 'MAJOR'
        else:
            return 'UNKNOWN'

    @property
    def first_commit(self):
        return self.tails[0]

    @property
    def __start_commit(self):
        """
        The start commit of a release is the first commit
        if the release has at least one commit, or the head
        if the release has no commit.
        """
        if self.tails:
            return self.first_commit
        else:
            return self.head

    @property
    def length(self):
        # return self.time - self.__start_commit.time
        return self.time - self.__start_commit.author_time


class Tag:
    """Tag

    Attributes:
        name: tag name
        commit: tagged commit
        time: tag time
        message (str): tag message - annotated tags only
    """

    def __init__(self):
        self.name = None
        self.commit = None
        self.time = None
        self.message = None


class Commit:
    """
    Commit

    Attributes:
        id: commit id
        message: commit message
        subject: first line from commit message
        commiter: contributor responsible for the commit
        author: contributor responsible for the code
        time: commit time
        author_time: author time
        release: associated release
    """

    def __init__(self):
        self.id = None
        self.subject = None
        self.message = None
        self.committer = None
        self.author = None
        self.release = None
        self.time = None
        self.author_time = None

    @property
    def parents(self):
        return []



class DeveloperDB:
    """
    Store developer information and handle developers with multiple ids
    """

    def __init__(self):
        self._developer_db = {}

    def load_developer(self, login=None, name=None, email=None):
        if not login:
            login = email
        if login not in self._developer_db:
            developer = Developer()
            developer.login = login
            developer.name = name
            developer.email = email
            self._developer_db[login] = developer
        return self._developer_db[login]

class Developer:
    """
    Contributors: Developers and committers

    Attributes:
        login: contributor id
        name: contributor name
        email: contributor e-mail
    """

    def __init__(self):
        self.login = None
        self.name = None
        self.email = None


def is_release_tag(project, tagname):
    """ Check if a tag represents a release """
    if project.release_pattern.match(tagname):
        return True
    return False


def is_tracked_commit(commit):
    """ Check if commit is tracked on a release """
    if commit.release:
        return True
    return False


def track_release(project, release):
    """
    Associate release to it commits

    Params:
        release: release list sorted by date
    """

    commit_stack = [ release.head ]
    while len(commit_stack):
        cur_commit = commit_stack.pop()

        # handle multiple tags pointing to a single commit
        if not is_tracked_commit(cur_commit):
            track_commit(project, release, cur_commit)

            is_tail = False
            if cur_commit.parents:
                for parent_commit in cur_commit.parents:
                    if is_tracked_commit(parent_commit):
                        is_tail = True
                    else:
                        commit_stack.append(parent_commit)
            else:
                is_tail = True
            if is_tail:
                release.tails.append(cur_commit)

    # release.tails = sorted(release.tails, key=lambda commit: commit.time)
    release.tails = sorted(release.tails, key=lambda commit: commit.author_time)


def track_commit(project, release, commit):
    " associate commit to release "
    commit.release = release
    release.commits.append(commit)
    if len(commit.parents) > 1:
        release.merges.append(commit)

    if commit.committer not in release.developers:
        release.developers.append(commit.committer)
    if commit.committer not in release.committers:
        release.committers.append(commit.committer)

    if commit.author not in release.developers:
         release.developers.append(commit.author)
    if commit.author not in release.authors:
        release.authors.append(commit.author)
    if commit.author not in project.authors:
        project.authors.append(commit.author)
        release.newcommers.append(commit.author)
