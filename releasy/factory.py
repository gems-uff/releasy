from pygit2 import Repository

from releasy.entity import Project
from releasy.entity import Release
from releasy.config import Config

class ProjectFactory():
    """ Factory that creates projects """
    def __init__(self):
        self.release_factory = None
        self.issue_factory = IssueFactory()

    def create(self, path):
        """ Creates a project """
        project = Project()
        repo = Repository(path)

        tag_refs = [ref for ref in repo.references if ref.startswith('refs/tags/')]
        commits_with_tags = {}
        for tag_ref in tag_refs:
            tag_ref = repo.lookup_reference(tag_ref)
            commit = tag_ref.peel()
            commits_with_tags[commit.hex] = 1

        commit_factory = CommitFactory()
        self.release_factory = ReleaseFactory(commit_factory, commits_with_tags)

        for tag_ref in tag_refs:
            tag_ref = repo.lookup_reference(tag_ref)

            if tag_ref.shorthand: # if is release
                release = self.release_factory.create(tag_ref)
                project[release] = release

        return project
        # parse git

class ReleaseFactory():
    """ Factory that creates releases """

    def __init__(self, commit_factory, commits_with_tags):
        self.commit_factory = commit_factory
        self.commits_with_tags = commits_with_tags

    def create(self, tag_ref):
        release = None

        commit_stack = [tag_ref.peel()]
        while commit_stack:
            cur_commit = commit_stack.pop()

            for parent_commit in cur_commit.parents:
                if parent_commit.hex in self.commits_with_tags:
                    print("stop")
                else:
                    commit_stack.append(parent_commit)

        return release

class IssueFactory():
    """ Factory that creates issues """
    pass

class CommitFactory():
    """ Factory that creates commits """
    pass