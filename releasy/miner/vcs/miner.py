# Module responsible to parse code repositories and mine releases and related
# information
#
import os.path

from ...model import Project, Commit
from ...release import ReleaseFactory, Release

class Miner():
    """ Mine a single repository """

    def __init__(self, vcs):
        name = os.path.basename(vcs.path)
        self._vcs = vcs
        self._project = Project(name)
        self._release_factory = ReleaseFactory()

    def mine_releases(self):
        """ Mine release related information, skipping commits """
        releases = []
        tags = sorted(self._vcs.tags(), key=lambda tag: tag.time)
        for tag in tags:
            release = self._release_factory.get_release(tag)
            if release:
                releases.append(release)
                tag.release = release

        self._project._tags = tags
        self._project._releases = releases
        return self._project

    def mine_commits(self) -> Project:
        """ Mine commit and associate related information to releases """
        if not self._project.releases:
            self.mine_releases()

        for release in self._project.releases:
            self._track_release(release)
        
        return self._project

    def _track_release(self, release: Release):
        commit_stack = [ release.head_commit ]
        while len(commit_stack):
            commit = commit_stack.pop()
            if not self._is_tracked_commit(commit):
                self._track_commit(release, commit)

                if commit.parents:
                    for parent in commit.parents:
                        if self._is_tracked_commit(parent):
                            if parent.release != release and parent.release not in release.base_releases:
                                release.base_releases.append(parent.release)
                            release._tail_commits.append(commit)
                        else:
                            commit_stack.append(parent)
                else: # root commit
                    release._tail_commits.append(commit)

        if len(release._commits) == 0: # releases that point to tracked commit
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
        release._tail_commits = sorted(release._tail_commits, key=lambda commit: commit.author_time)

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
        release._commits.append(commit)
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
