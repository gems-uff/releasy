#
#
#
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List

from .release import Release
from .model import Tag, Commit
from .miner.vcs.miner import Vcs
from .data import Release

class ReleaseMineStratety:
    """Mine releases bases on a strategy. It discover the releases. """

    def __init__(self, vcs: Vcs):
        self.vcs = vcs

    def mine_releases(self) -> List[Release]:
        """ Mine the releases 

        :return: the list of releases in reverse cronological order
        """
        pass


class CommitMineStrategy:
    """ Mine release commits based on a strategy. It assign commits to 
    releases """

    def __init__(self, vcs: Vcs, releases: List[Release]):
        self.vcs = vcs
        self.releases = releases

    def mine_commits():
        pass


class ReleaseMatcher:
    """ Check if tag is a release """

    def is_release(self, tag: Tag) -> bool:
        pass


class TrueReleaseMatcher:
    """ Matcher that consider all tags as releases """

    def is_release(self, tag: Tag) -> bool:
        return True


class TagReleaseMineStrategy(ReleaseMineStratety):
    """ Mine tags for releases """

    def __init__(self, vcs: Vcs, release_matcher: ReleaseMatcher):
        super().__init__(vcs)
        self.matcher = release_matcher

    def mine_releases(self) -> List[Release]:
        """ Discover releases """
        # Tags can reference any git object. For release detectioin purpouse, 
        # we only need tags that reference commits
        tags = [tag for tag in self.vcs.tags() if tag.commit]
        tags = sorted(tags, key=lambda tag: tag.time, reverse=True)
        releases = []
        for tag in tags:
            if self.matcher.is_release(tag):
                release = Release(tag)
                releases.append(release)
        return releases


class HistoryMineStrategy(CommitMineStrategy):
    """ Mine releases based on the commit history. It walk through the commit
    parents to retrieve the commit history and split them based on the 
    releases found in its history. """ 

    def __init__(self, vcs: Vcs, releases: List[Release]):
        super().__init__(vcs, releases)
        self.release_index = {}

    def mine_commits(self):
        releases = sorted(self.releases, key=lambda release: release.time)
        for release in releases:
            self.release_index[release.head.id] = True

        release_commits = {}
        for release in releases:
            commits = self._track_commits(release)
            release_commits[release.name] = commits
        return release_commits
    
    def _track_commits(self, release: Release) -> List[Commit]:
        commit_index = {}
        commits = []
        commit_stack = [ release.head ]
        while len(commit_stack):
            commit = commit_stack.pop()
            if commit.id not in commit_index:
                commits.append(commit)
                commit_index[commit.id] = True

                if commit.parents:
                    for parent in commit.parents:
                        if not parent.id in self.release_index:
                            commit_stack.append(parent)

        commits = sorted(commits, key=lambda commit: commit.committer_time, reverse=True)
        return commits


class TimeMineStrategy(CommitMineStrategy):
    """ Mine releases based on the tag time. It sorts the commits in reverse 
    cronological order and split them based on the release date. """ 

    def __init__(self, vcs: Vcs, releases: List[Release]):
        super().__init__(vcs, releases)
        self.release_index = {}
        
    def mine_commits(self):
        releases = sorted(self.releases, key=lambda release: release.time)
        commits = sorted(self.vcs.commits(), key=lambda commit: commit.committer_time)

        release_commits = {}
        commit_index = 0
        for release in releases:
            cur_release_commits = []
            release_end = release.head.committer_time
            
            release_has_commits = True
            while release_has_commits:
                if commits[commit_index].committer_time <= release_end:
                    cur_release_commits.append(commits[commit_index])
                    commit_index += 1
                else:
                    release_has_commits = False

            cur_release_commits = sorted(cur_release_commits, key=lambda commit: commit.committer_time, reverse=True)
            release_commits[release.name] = cur_release_commits

        return release_commits

