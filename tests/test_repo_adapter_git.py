import pytest
from releasy.repository import Commit, Repository, Tag

from releasy.repo_adapter_git import GitCommitAdapter, GitRepoAdapter, GitTagAdapter


class describe_git_tag_adapter:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = Repository(GitRepoAdapter('.'))
        self.tag_adapter = GitTagAdapter(self.repository)

    def it_has_tags(self):
        tags = self.tag_adapter.get_tags()
        assert tags

    def it_has_specific_tags(self):
        tags = self.tag_adapter.get_tags()
        assert Tag(self.repository, '1.0.1') in tags
        # TODO assert '1.0.1' in tags

class describe_git_commit_adapter:
    @pytest.fixture(autouse=True)
    def init(self):
        self.commit_adapter = GitCommitAdapter(GitRepoAdapter('.'))

    def it_has_specific_commits(self):
        assert \
            Commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db') \
            == self.commit_adapter.get_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')


