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

    def __init__(self, path):
        self.path = path
        self.releases = []  #: list of project releases
                            #: regexp to match release name
        self.release_pattern = re.compile(r'(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?.*')
        self.__vcs = None

    @property
    def vcs(self):
        return self.__vcs

    @vcs.setter
    def vcs(self, vcs):
        self.__vcs = vcs
        self.__vcs.path = self.path

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
            if is_release_tag(self, tagname):
                tag = self.vcs.load_tag(tagname)
                self.releases.append(Release(self, tag))
        self.releases = sorted(self.releases, key=lambda release: release.time)

    def __load_commits(self):
        for release in self.releases:
            track_release(release)

    @staticmethod
    def create(path, vcs):
        project = Project(path)
        project.vcs = vcs
        project.load()
        return project


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """

    def __init__(self):
        self._commit_cache = {}
        self._tag_cache = {}

    def fetch_commit(self, id, commit = None):
        if id not in self.__commit_dict and commit:
            self.__commit_dict[id] = commit
        return self.__commit_dict[id]

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
        tag: tag that represents the release
        head: commit referred  by release.tag
        tails: list of commits where the release begin
    """

    def __init__(self, project, tag):
        self.project = project
        self.tag = tag
        self.commits = []
        self.tails = []

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
    def duration(self):
        return self.time - self.__start_commit.time


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


class Contributor:
    """
    Developers and committers

    Attributes:
        name: contributor name
        email: contributor e-mail
    """

    def __init__(self):
        self.name = None    #: contributor name
        self.email = None   #: contributor e-mail


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


def track_release(release):
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
            cur_commit.release = release
            release.commits.append(cur_commit)

            is_tail = False
            for parent_commit in cur_commit.parents:
                if is_tracked_commit(parent_commit):
                    is_tail = True
                else:
                    commit_stack.append(parent_commit)
            if is_tail:
                release.tails.append(cur_commit)

    release.tails = sorted(release.tails, key=lambda commit: commit.time)


