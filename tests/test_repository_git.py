from datetime import datetime, timezone
import pytest
from releasy.repository import Commit, Repository, Tag

from releasy.repository_git import GitRepository

@pytest.mark.local
class describe_git_repository:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = Repository(GitRepository('.'))

    def it_fetch_tags(self):
        tags = self.repository.get_tags()
        assert tags
        assert len(tags) > 10
        assert Tag(self.repository, '1.0.1') in tags
        # TODO assert '1.0.1' in tags

    def it_has_specific_commits(self):
        assert self.repository.get_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')

    def it_fetch_parents(self):
        commit = self.repository.get_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')
        assert commit.parents.ids \
            == set(['f45fb10eb1354c7a4ff421b07598e008e8ad427b'])

    def it_mine_time(self):
        commit = self.repository.get_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')
        # Fri May 27 22:03:48 2022 -0300
        # Sat May 28 01:03:48 2022
        assert commit.committer_time \
            == datetime(2022, 5, 28, 1, 22, 49, tzinfo=timezone.utc) 
        assert commit.author_time \
            == datetime(2022, 5, 28, 1, 3, 48, tzinfo=timezone.utc) 
