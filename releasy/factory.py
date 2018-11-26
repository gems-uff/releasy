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

        loop_detection = {}
        commit_stack = [tag_ref.peel()]
        while commit_stack:
            cur_commit = commit_stack.pop()
            loop_detection[cur_commit.hex] = 1

            commit = self.commit_factory.create(cur_commit)
#            release[commit.hash] = commit

            for parent_commit in cur_commit.parents:
                if parent_commit.hex in self.commits_with_tags:
                    pass # add base
                elif parent_commit.hex not in loop_detection.keys():
                    commit_stack.append(parent_commit)
                else:
                    print('loop ', parent_commit.hex)

        return release

class IssueFactory():
    """ Factory that creates issues """
    pass

class CommitFactory():
    """ Factory that creates commits """
    def __init__(self):
        self.commit_map = {}
        self.developer_map = {}

    def __create_commit(self, raw_commit):
        if raw_commit.hex in self.commit_map.keys():
            return self.commit_map[raw_commit.hex]
        else:
            return Commit(
            hash=raw_commit.hex,
            subject=raw_commit.message
            commiter=
            developer=
            commit_time=
            devepment_time=
        )


    def create(self, raw_commit):
        commit = self.__create_commit(raw_commit)

        Commit(object):

        # old
        def __init__(self, hash, subject=None, parent=None, commiter=None,
                     developer=None, commit_time=None, development_time=None):
            self.hash = hash
            self.subject = subject
            self.parent = parent
            self.commiter = commiter
            self.commit_time = commit_time
            self.developer = developer
            self.development_time = development_time
            self.issues = []

            self.__tags = []
            # todo remove:
            self.release = []
