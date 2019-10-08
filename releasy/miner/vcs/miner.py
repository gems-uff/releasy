# Module responsible to parse code repositories and mine releases and related
# information
#
import os.path

from ...model import Project, Commit
from ...release import ReleaseFactory, Release

class Miner():
    """ Mine a single repository """

    def __init__(self, vcs, release_prefixes=None):
        name = os.path.basename(vcs.path)
        self._vcs = vcs
        self._project = Project(name)
        self._release_factory = ReleaseFactory(self._project, prefixes=release_prefixes)

    def mine_releases(self):
        """ Mine release related information, skipping commits """
        releases = []
        feature_release = {}

        #TODO sort per graph position
        tags = sorted(self._vcs.tags(), key=lambda tag: tag.time)
        for tag in tags:
            release = self._release_factory.get_release(tag)
            if release:
                releases.append(release)
                if not release.is_patch():
                    feature_release[release.feature_version] = release

        previous_release = None
        previous_feature_release = None
        for release in releases:
            if release.is_patch() and release.feature_version in feature_release:
                feature_release[release.feature_version].patches.append(release)
            
            if previous_release:
                previous_release.next_release = release
            release.previous_release = previous_release
            previous_release = release
            
            release.previous_feature_release = previous_feature_release
            if not release.is_patch() and not release.is_pre_release():
                previous_feature_release = release

        for release in feature_release.values():
            release.patches = sorted(release.patches, key=lambda release: release.time)

        self._project.tags = tags
        self._project._releases = releases
        return self._project

    def mine_commits(self) -> Project:
        """ Mine commit and associate related information to releases """
        if not self._project.releases:
            self.mine_releases()

        for release in self._project.releases:
            self._track_release(release)
            release.add_commits_from_pre_releases()

        return self._project

    def _track_release(self, release: Release):
        commit_stack = [ release.head_commit ]
        while len(commit_stack):
            commit = commit_stack.pop()
            if not commit.has_release():
                release.add_commit(commit)

                if commit.parents:
                    for parent in commit.parents:
                        if parent.has_release() and parent.release != release:
                            self._track_base_release(release, parent)
                            release.tail_commits.append(commit)
                        else:
                            commit_stack.append(parent)
                else: # root commit
                    #TODO create aadd method
                    release.tail_commits.append(commit)

        if len(release.commits) == 0: # releases that point to tracked commit
            commit = release.head_commit
            release.base_releases.append(commit.release)

        # Remove base releases reachable by other base releases
        for base_release in release.base_releases:
            release.reachable_releases.extend(base_release.reachable_releases)
        base_release_to_remove = []
        for base_release in release.base_releases:
            if base_release in release.reachable_releases:
                base_release_to_remove.append(base_release)
        for base_release in base_release_to_remove:
            release.base_releases.remove(base_release)
        release.reachable_releases += release.base_releases
        release.reachable_releases = list(set(release.reachable_releases))

        release.base_releases = sorted(release.base_releases, key=lambda release: release.version)
        release.reachable_releases = sorted(release.reachable_releases, key=lambda release: release.version)
        release.tail_commits = sorted(release.tail_commits, key=lambda commit: commit.author_time)

    def _track_base_release(self, release, commit):
        commit_stack = [ commit ]
        visited_commit = set()
        while len(commit_stack):
            commit = commit_stack.pop()
            visited_commit.add(commit)
            if commit.release and commit.release.head_commit == commit:
                if commit.release not in release.base_releases:
                    release.base_releases.append(commit.release)
            else:
                for parent in commit.parents:
                    if parent not in visited_commit:
                        commit_stack.append(parent)


class Vcs:
    """
    Version Control Repository

    Attributes:
        __commit_dict: internal dictionary of commits
    """
    def __init__(self, path):
        self.path = path
        self._tags = []

    def tags(self):
        """ Return repository tags """
        return self._tags

