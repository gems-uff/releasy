# Module responsible to parse code repositories and mine releases and related
# information
#

import os.path
import re

from .model import Project, Release, Commit


class Miner():
    """ Mine a single repository """

    def __init__(self, vcs):
        name = os.path.basename(vcs.path)
        self._vcs = vcs
        self._project = Project(name)

    def mine_releases(self):
        """ Mine release related information, skipping commits """
        releases = []
        for tag in self._vcs.tags():
            (is_release, release_type, prefix, major, minor, patch) = self._match_release(tag.name)
            if is_release:
                release = Release(tag,
                                  release_type=release_type,
                                  prefix=prefix,
                                  major=major,
                                  minor=minor,
                                  patch=patch)

                releases.append(release)
        releases = sorted(releases, key=lambda release: release.version)
        self._project._releases = releases
        return self._project

    def mine_commits(self):
        """ Mine commit and associate related information to releases """
        if not self._project.releases:
            self.mine_releases()

        for release in self._project.releases:
            self._track_release(release)
        
        return self._project

    def _track_release(self, release):
        commit_stack = [ release.head_commit ]
        while len(commit_stack):
            commit = commit_stack.pop()
            if not self._is_tracked_commit(commit):
                self._track_commit(release, commit)

                if commit.parents:
                    for parent in commit.parents:
                        if self._is_tracked_commit(parent):
                            release.base_releases.append(parent.release)
                            release.tail_commits.append(commit)
                        else:
                            commit_stack.append(parent)
                else: # root commit
                    release.tail_commits.append(commit)

        if release.commits.count() == 0: # releases that point to tracke commits
            commit = release.head_commit
            release.base_releases.append(commit.release)

        release.base_releases = sorted(release.base_releases, key=lambda release: release.version)
        release.tail_commits = sorted(release.tail_commits, key=lambda commit: commit.author_time)

        return self._project

    def _is_tracked_commit(self, commit):
        """ Check if commit is tracked on a release """
        if commit.release:
            return True
        else:
            return False

    def _track_commit(self, release, commit):
        """ associate commit to release """
        committer = commit.committer
        author = commit.author
        commit.release = release
        release.commits.add(commit)
        self._project.commits.add(commit)

        release.developers.committers.add(committer, commit)
        release.developers.authors.add(author, commit)
        release.developers.add(committer, commit)
        if not self._project.developers.contains(committer):
            release.developers.newcomers.add(committer, commit)
        self._project.developers.committers.add(committer, commit)
        self._project.developers.add(committer, commit)
        if not self._project.developers.contains(author):
            release.developers.newcomers.add(author, commit)
        self._project.developers.authors.add(author, commit)
        if committer != author:
            release.developers.add(author, commit)
            self._project.developers.add(author, commit)

    def _match_release(self, tagname):
        pattern = re.compile(r'^(?P<prefix>(?:.*?[^0-9\.]))?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)(-(?P<pre>.+))?$')
        re_match = pattern.search(tagname)
        if re_match:
            prefix = re_match.group('prefix')
            major_version = 0
            minor_version = 0
            patch_version = 0
            pre_release = re_match.group('pre')

            major = re_match.group('major')
            if major:
                major_version = int(major)

            minor = re_match.group('minor')
            if minor:
                minor_version = int(minor)

            patch = re_match.group('patch')
            if patch:
                patch_version = int(patch)

            if patch_version > 0:
                release_type = 'PATCH'
            elif minor_version > 0:
                release_type = 'MINOR'
            elif major_version > 0:
                release_type = 'MAJOR'

            return (True,
                    release_type,
                    prefix,
                    major_version,
                    minor_version,
                    patch_version)
        else:        
            return False


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """
    def __init__(self, path):
        self.path = path

    def tags(self):
        """ Return repository tags """
        pass

    def commits(self):
        """ Return repository commits """
        pass
