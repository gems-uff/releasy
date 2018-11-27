import os
import yaml
import re

from pygit2 import Repository

from releasy.entity import Project, Issue, Release, Tag, Commit, Developer, Tag
from releasy.config import Config

class ProjectFactory():
    """ Factory that creates projects """
    def create(self, path):
        """ Creates a project """
        config = Config(base_dir=path)
        project = Project(config)

        developer_factory = DeveloperFactory()
        commit_factory = CommitFactory(developer_factory)
        issue_factory = IssueFactory()

        if os.path.exists(config.issues_file):
            with open(config.issues_file, 'r') as stream:
                try:
                    raw_issues = yaml.load(stream)
                    for raw_issue in raw_issues:
                        issue = issue_factory.create(raw_issue)
                        project.add_issue(issue)
                except yaml.YAMLError as exc:
                    print(exc)
                    raise

        repo = Repository(path)
        tag_refs = [ref for ref in repo.references if ref.startswith('refs/tags/')]
        commits_with_tags = {}
        for tag_ref in tag_refs:
            raw_tag = repo.lookup_reference(tag_ref)
            commit = raw_tag.peel()
            commits_with_tags[commit.hex] = raw_tag

        release_factory = ReleaseFactory(commit_factory, commits_with_tags)

        for tag_ref in tag_refs:
            tag_ref = repo.lookup_reference(tag_ref)
            if tag_ref.shorthand: # if is release
                release = release_factory.create(tag_ref)
                project[release] = release

        return project

class ReleaseFactory():
    """ Factory that creates releases """

    def __init__(self, commit_factory, commits_with_tags):
        self.commit_factory = commit_factory
        self.commits_with_tags = commits_with_tags
        self.release_map = {}
        self.linked_commits = {}

    def create(self, raw_tag, iterate=True):
        raw_release_tag_commit = raw_tag.peel()

        if raw_tag.name not in self.release_map:
            release_tag_commit = self.commit_factory.create(raw_release_tag_commit)
            release_tag = Tag(raw_tag.shorthand, release_tag_commit) #todo create TagFactory
            self.release_map[raw_tag.name] = Release(release_tag)
        release = self.release_map[raw_tag.name]

        if iterate:
            loop_detection = {}
            commit_stack = [raw_release_tag_commit]
            while commit_stack:
                cur_commit = commit_stack.pop()
                loop_detection[cur_commit.hex] = 1

                commit = self.commit_factory.create(cur_commit)

                # find related issues #todo
                if cur_commit.hex not in self.linked_commits:
                    issue_match = re.search(r'#([0-9]+)', commit.subject)
                    issue = None
                    if issue_match:
                        issue_id = int(issue_match.group(1))
                        issue = self.get_issue(issue_id)
                        if issue not in commit.issues:
                            commit.add_issue()

                            commit.issues.append(issue)
                            issue.commits.append(commit)
                    self.linked_commits[cur_commit.hex] = 1

                # link commits
                release[commit.hash] = commit
                commit.releases.append(release)

                for parent_commit in cur_commit.parents:
                    if parent_commit.hex in self.commits_with_tags:
                        base_release = self.create(
                            self.commits_with_tags[parent_commit.hex],
                            iterate=False
                        )
                        release.base_releases.append(base_release)
                    elif parent_commit.hex not in loop_detection.keys():
                        commit_stack.append(parent_commit)
                    #todo else: loop detected

            release.commits = sorted(release.commits, key=lambda commit: commit.commit_time)

        return release


class IssueFactory():
    """ Factory that creates issues """
    def create(self, raw_issue):
        # todo
        return Issue(
            id=raw_issue['id'],
            subject=raw_issue['subject'],
            labels=raw_issue['labels']
        )


class CommitFactory():
    """ Factory that creates commits """
    def __init__(self, developer_factory):
        self.commit_map = {}
        self.incomplete_commit_map = {}
        self.developer_factory = developer_factory

    def create(self, raw_commit, hash_only=False):
        if raw_commit.hex not in self.commit_map:
            self.commit_map[raw_commit.hex] = Commit(
                hash=raw_commit.hex,
            )
            self.incomplete_commit_map[raw_commit.hex] = True

        if not hash_only and raw_commit.hex in self.incomplete_commit_map:
            commit = self.commit_map[raw_commit.hex]
            author = self.developer_factory.create(raw_commit.author)
            committer = self.developer_factory.create(raw_commit.committer)
            commit.subject = raw_commit.message
            commit.committer = committer
            commit.commit_time = raw_commit.commit_time
            commit.author = author
            commit.author_time = raw_commit.author.time
            del self.incomplete_commit_map[raw_commit.hex]

            for raw_parent in raw_commit.parents:
                commit.parents.append(self.create(raw_parent, hash_only=True))

        return self.commit_map[raw_commit.hex]


class DeveloperFactory():
    """ Factory that creates contributors """
    def __init__(self):
        self.developer_map = {}

    def create(self, raw_developer):
        if raw_developer.email not in self.developer_map:
            self.developer_map[raw_developer.email] = Developer(
                name=raw_developer.name,
                email=raw_developer.email
            )

        return self.developer_map[raw_developer.email]
