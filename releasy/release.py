import re
from datetime import timedelta

from .model import Tag, CommitTracker
from .developer import DeveloperRoleTracker

class ReleaseFactory():
    def __init__(self):
        self._pre_release_cache = {}

    def get_release(self, tag: Tag):
        release_info = self._match_release(tag.name)
        if not release_info:
            return None
        else:
            (release_type, prefix, major, minor, patch) = release_info
            release_version = "%d.%d.%d" % (major, minor, patch)
            if release_version not in self._pre_release_cache:
                self._pre_release_cache[release_version] = []

            if release_type == "PRE":
                release = PreRelease(tag=tag, release_type="PRE", prefix=prefix, major=major, minor=minor, patch=patch)
                self._pre_release_cache[release_version].append(release)
            else:
                release = Release(tag=tag, 
                                  release_type="release_type",
                                  prefix=prefix, 
                                  major=major, 
                                  minor=minor, 
                                  patch=patch,
                                  pre_releases = self._pre_release_cache[release_version])

            return release

    def _match_release(self, tagname):
        pattern = re.compile(r"^(?P<prefix>(?:.*?[^0-9\.]))?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)(-(?P<pre>.+))?$")
        re_match = pattern.search(tagname)
        if re_match:
            prefix = re_match.group("prefix")
            major_version = 0
            minor_version = 0
            patch_version = 0
            pre_release = re_match.group("pre")

            major = re_match.group("major")
            if major:
                major_version = int(major)

            minor = re_match.group("minor")
            if minor:
                minor_version = int(minor)

            patch = re_match.group("patch")
            if patch:
                patch_version = int(patch)

            if pre_release:
                release_type = "PRE"
            elif patch_version > 0:
                release_type = "PATCH"
            elif minor_version > 0:
                release_type = "MINOR"
            elif major_version > 0:
                release_type = "MAJOR"

            return (release_type,
                    prefix,
                    major_version,
                    minor_version,
                    patch_version)
        else:        
            return False


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
        developers: list of developers
        length: release duration
    """

    def __init__(self, tag, release_type=None, prefix=None, major=None, minor=None, patch=None, pre_releases=None):
        self._tag = tag
        self.type = release_type
        self.prefix = prefix
        self.major = major
        self.minor = minor
        self.patch = patch
        self.version = "%d.%d.%d" % (self.major, self.minor, self.patch)
        self.base_releases = []
        self.reachable_releases = []
        self._tail_commits = []
        self._commits = []
#        self.commits = CommitTracker()
        self.developers = DeveloperRoleTracker()
        self.pre_releases = pre_releases
        
    @property
    def name(self):
        return self._tag.name
        
    @property
    def head_commit(self):
        return self._tag.commit

    @property
    def commits(self):
        commits = [] + self._commits
        for pre_release in self.pre_releases:
            commits += pre_release.commits
        return commits

    @property
    def tail_commits(self):
        tail_commits = [] + self._tail_commits
        for pre_release in self.pre_releases:
            tail_commits += pre_release.tail_commits
        tail_commits = sorted(tail_commits, key=lambda commit: commit.author_time)
        return tail_commits

    @property
    def time(self):
        return self._tag.time

    @property
    def length(self):
        #TODO consider tag length
        if self.tail_commits:
            return self.time - self.tail_commits[0].author_time
        else:
            return timedelta(0)

    @property
    def description(self):
        return self._tag.message

    def __repr__(self):
        return self.name

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
    def length_group(self):
        if self.length < timedelta(hours=1):
            return 0 #'minutes'
        elif self.length < timedelta(days=1):
            return 1 #'hours'
        elif self.length < timedelta(days=7):
            return 2 #'days'
        elif self.length < timedelta(days=30):
            return 3 #'weeks'
        elif self.length < timedelta(days=365):
            return 4 #'months'
        else:
            return 5 #'years'

    @property
    def length_groupname(self):
        return {
            0: 'minutes',
            1: 'hours',
            2: 'days',
            3: 'weeks',
            4: 'months',
            5: 'years'
        }[self.length_group]
    
    @property
    def churn(self):
        if self.__commit_stats:
            return self.__commit_stats.churn

        self.__commit_stats = CommitStats()
        if self.base_releases:
            for base_release in self.base_releases:
                self.__commit_stats += self.head.diff_stats(base_release.head)
        else:
            self.__commit_stats = self.head.diff_stats()

        return self.__commit_stats.churn


class PreRelease(Release):
    def __init__(self, tag, release_type=None, prefix=None, major=None, minor=None, patch=None):
        super().__init__(tag=tag, release_type=release_type, prefix=prefix, major=major, minor=minor, patch=patch)

    @property
    def commits(self):
        return self._commits
    
    @property
    def tail_commits(self):
        return self._tail_commits


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

    def __repr__(self):
        return self.login
