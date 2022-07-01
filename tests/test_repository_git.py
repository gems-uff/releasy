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

    def it_mine_tag_time(self):
        tags = sorted(self.repository.get_tags(), key=lambda tag: tag.time)
        # 1.0.0 1.0.1 Sep 18 00:12:14 2018 -0300
        assert tags[0].time == tags[1].time
        assert tags[1].time \
            == datetime(2018, 9, 18, 3, 12, 14, tzinfo=timezone.utc)
        # 3.0.1 Oct 31 16:04:09 2021
        assert tags[16].time \
            == datetime(2021, 10, 31, 16, 4, 9, tzinfo=timezone.utc)

    def it_mine_annotated_tags(self):
        tags = sorted(self.repository.get_tags(), key=lambda tag: tag.time)
        assert tags[0].is_annotated #1.0.0
        assert not tags[16].is_annotated #3.0.1

    def it_mine_tag_commits(self):
        tags = sorted(self.repository.get_tags(), key=lambda tag: tag.time)
        assert tags[0].commit.id == '6cbc4690fde818f063cde972192fedd1f5f7d4cd'
        assert tags[16].commit.id == '08aee17c59f742e57518b69d0bd2c452e905e109'

    def it_mine_tag_author(self):
        tags = sorted(self.repository.get_tags(), key=lambda tag: tag.time)
        assert tags[0].author == 'Felipe Curty <felipecrp@gmail.com>'
        assert tags[16].author == None

    def it_mine_commit_time(self):
        commit = self.repository.get_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')
        # Fri May 27 22:03:48 2022 -0300
        # Sat May 28 01:03:48 2022
        assert commit.committer_time \
            == datetime(2022, 5, 28, 1, 22, 49, tzinfo=timezone.utc) 
        assert commit.author_time \
            == datetime(2022, 5, 28, 1, 3, 48, tzinfo=timezone.utc) 

    def it_mine_diff(self):
        commit_a = self.repository.get_commit('18a0198d91cfa21b27ea6fa60353a606ba76c7db')
        commit_b = self.repository.get_commit('f45fb10eb1354c7a4ff421b07598e008e8ad427b')
        diff_delta = commit_a.diff(commit_b)

        assert diff_delta.insertions == 180
        assert diff_delta.deletions == 190
        assert diff_delta.files_changed == 4
        assert diff_delta.churn == 370
