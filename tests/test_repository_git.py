import pytest
from releasy.repository import Commit, Repository, Tag

from releasy.repository_git import GitRepository


class describe_git_repository:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = GitRepository('.')

    def it_fetch_tags(self):
        tags = self.repository.fetch_tags()
        assert tags
        assert len(tags) > 10
        assert Tag(None, '1.0.1') in tags
        # TODO assert '1.0.1' in tags

    def it_has_specific_commits(self):
        assert \
            Commit(None, '18a0198d91cfa21b27ea6fa60353a606ba76c7db') \
            == self.repository.fetch_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')

    def it_fetch_parents(self):
        commit = self.repository.fetch_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')
        assert \
            Commit(None, 'f45fb10eb1354c7a4ff421b07598e008e8ad427b') \
            in self.repository.fetch_commit_parents(commit)
