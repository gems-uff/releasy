import pytest
from releasy.repository import Commit, Repository, Tag

from releasy.repository_git import GitRepository


class describe_git_repository:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = GitRepository('.')

    def it_has_tags(self):
        tags = self.repository.fetch_tags()
        assert tags

    def it_has_specific_tags(self):
        tags = self.repository.fetch_tags()
        assert Tag(self.repository, '1.0.1') in tags
        # TODO assert '1.0.1' in tags

class describe_git_commit_adapter:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = GitRepository('.')

    def it_has_specific_commits(self):
        assert \
            Commit(None, '18a0198d91cfa21b27ea6fa60353a606ba76c7db') \
            == self.repository.fetch_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')


