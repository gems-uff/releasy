# Module responsible to mine code repositories and extract releases information
#
import os.path

import releasy
from ...model import Project, Commit
from ...release import ReleaseFactory, Release

class Miner():
    """ 
    Mine a single repository 
    
    This class is responsible for mining an repository and extrat all available 
    release information.
    """
    def __init__(self, vcs, name=None, release_prefixes=None, ignored_suffixes=None, version_separator=None, track_base_release=True):
        if not name:
            name = os.path.basename(vcs.path)
        self._vcs = vcs
        self._project = Project(name)
        self._release_factory = ReleaseFactory(
            self._project,
            prefixes=release_prefixes,
            ignored_suffixes=ignored_suffixes,
            version_separator=version_separator
        )
        self.track_base_release = track_base_release
        # ---
        self._releases = [] #TODO use project._releases
        self._commit_references = {} # Commit Hash -> Release

    def mine(self, skip_commit = False):
        """ Mine the software repository
        
        Parameters:
            skip_commit (bool): if true, the miner will ignore the release 
            history. This parameter is usefull when only tag information is 
            needed.

        Returns:
            The project with all release metadas
        """
        self.mine_releases()
        if not skip_commit:
            self.mine_commits()
        return self._project

    def mine_releases(self):
        """ Mine release related information, skipping commits """
        tags = [tag for tag in self._vcs.tags() if tag.commit] #TODO add test to check nom commit tags
        tags = sorted(tags, key=lambda tag: tag.time)
        for tag in tags:
            main_release = self._get_main_release(tag)
            release = self._release_factory.build(tag, main_release)
            self._save_release(release)

        self._project.tags = tags
        self._project._assign_releases(self._releases)
        return self._project

    def _is_duplicated_reference(self, tag): #TODO eval move to Tag class
        """ Verify if the head commit is in used in another release """
        head_commit = tag.commit
        commit_ide = head_commit.hashcode
        if commit_ide in self._commit_references:
            return True
        else:
            return False

    def _get_main_release(self, tag): #TODO eval move to Tag class
        """ If the release is duplicated, return the original release """
        head_commit = tag.commit
        commit_ide = head_commit.hashcode
        if commit_ide in self._commit_references:
            return self._commit_references[commit_ide]
        else:
            return None

    def _save_release(self, release):
        if release:
            self._releases.append(release)
            head_commit = release.head_commit
            self._commit_references[head_commit.hashcode] = release

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
        if not self.track_base_release:
            return
            
        commit_stack = [ commit ]
        visited_commit = {}
        while len(commit_stack):
            commit = commit_stack.pop()
            visited_commit[commit.hashcode] = 1
            if commit.release and commit.release.head_commit == commit:
                if commit.release not in release.base_releases:
                    release.base_releases.append(commit.release)
            else:
                for parent in commit.parents:
                    if parent.hashcode not in visited_commit:
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

