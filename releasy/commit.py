from __future__ import annotations
from typing import TYPE_CHECKING, Set

if TYPE_CHECKING:
    from .release import Release

class Commit:
    """
    Commit

    Attributes:
        hashcode: commit id
        message: commit message
        subject: first line from commit message
        committer: contributor responsible for the commit
        author: contributor responsible for the code
        time: commit time
        author_time: author time
        release: associated release
    """
    def __init__(self, hashcode, parents=None, message=None,
                 author=None, author_time=None,
                 committer=None, committer_time=None):
        self.id = hashcode
        self.hashcode = hashcode
        self.parents = parents
        self.message = message
        self.author = author
        self.author_time = author_time
        self.committer = committer
        self.committer_time = committer_time
        self.releases: Set[Release] = set()
        self.tags: Set[Tag] = set()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        return False

    def has_release(self) -> bool:
        return bool(self.releases)

    def has_tags(self) -> bool:
        return bool(self.tags)

    def __repr__(self):
        return str(self.hashcode)

    def describe(self):
        raise NotImplementedError()

    def history(self, unreachable_by: Set[Commit] = None,
            include_self: bool = False):
        """
        Return the commits that the current commit can reach. 
        
        This method navigates through the commit history (using the parent
        relationship) and stops when reaches a commit that belongs to the
        history of a commit in the `unreachable_by` set.

        Parameters:
        unreachable_by : Set[Commit]
            The stop condition, i.e., when the method will stop navigating to 
            parent commits.
        include_self: bool
            Whether the history should includes the current commit or not
        """
        commits: Set(Commit) = set()
        if include_self:
            commits.add(self)
        
        commits_to_remove = set()
        if unreachable_by:
            commits_to_remove = set()
            for commit in unreachable_by:
                commits_to_remove |= commit.history(include_self=True)

        commits_to_track = [parent_commit for parent_commit in self.parents]
        while commits_to_track:
            commit = commits_to_track.pop()
            if commit not in commits and commit not in commits_to_remove:
                commits.add(commit)
                for parent_commit in commit.parents:
                    commits_to_track.append(parent_commit)
        return commits

    def release_history(self, include_self: bool = False):
        commits: Set(Commit) = set()
        if include_self:
            commits.add(self)
        
        base_commits = set()
        commits_to_track = [parent_commit for parent_commit in self.parents]
        while commits_to_track:
            commit = commits_to_track.pop()
            if commit not in commits:
                if commit.releases:
                    base_commits.add(base_commits)
                else:
                    commits.add(commit)
                    for parent_commit in commit.parents:
                        commits_to_track.append(parent_commit)

        for commit in base_commits:
            commits -= commit.history()

        return commits, base_commits


class Tag:
    """Tag

    Attributes:
        name: tag name
        commit: tagged commit
        time: tag time
        message (str): tag message - annotated tags only
    """

    def __init__(self, name, commit, time=None, message=None):
        self.name = name
        self.commit = commit
        commit.tags.add(self)
        self.release = None
        self.time = None
        self.message = None
        if time: # annotated tag
            self.is_annotated = True
            self.time = time
            self.message = message
        else:
            self.is_annotated = False
            if commit:
                self.time = commit.committer_time
                self.message = commit.message
    
    def __repr__(self):
        return self.name