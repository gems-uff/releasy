from datetime import timedelta
from typing import Set
import pytest
from releasy.repository import Commit, Repository, RepositoryProxy, Tag
from .mock_repository import MockRepository, MockRepositoryProxy


@pytest.fixture
def repo():
    return MockRepository()

class describe_tag:
    def it_has_repository(self, repo: Repository):
        tag = Tag(repo, '1.0.0')
        assert tag.repository

    def it_has_name(self, repo: Repository):
        tag = Tag(repo, '1.0.0')
        assert tag.name == '1.0.0'

    def it_has_commit(self, repo: Repository):
        tag = Tag(repo, '1.0.0', Commit(repo, '1'))
        assert Commit(repo, '1') == tag.commit


class describe_commit:
    def it_has_repository(self, repo: Repository):
        commit = Commit(repo, '1')
        assert commit.repository

    def it_has_id(self, repo: Repository):
        commit = Commit(repo, '1')
        assert commit.id == '1'

    def it_has_parents(self, repo: Repository):
        commit = repo.get_commit('14')
        assert commit.parents.ids == set(['12', '13'])

    def it_has_committer(self, repo: Repository):
        assert 'alice' == repo.get_commit('0').committer
        assert 'bob' == repo.get_commit('2').committer
        assert 'charlie' == repo.get_commit('7').committer

    def it_has_author(self, repo: Repository):
        assert 'alice' == repo.get_commit('0').author
        assert 'bob' == repo.get_commit('1').author
        assert 'charlie' == repo.get_commit('8').author

    def it_has_committer_time(self, repo: Repository):
        ref = repo.get_commit('0').committer_time
        assert repo.get_commit('10').committer_time == ref + 10*timedelta(days=1)

    def it_has_author_time(self, repo: Repository):
        ref = repo.get_commit('0').committer_time
        assert repo.get_commit('10').committer_time == ref + 10*timedelta(days=1)
        

class describe_repository:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = MockRepository()

    def it_fetch_tags(self):
        tags = self.repository.get_tags()
        assert len(tags) == 18
        assert Tag(self.repository, '1.1.0') in tags

    def it_fetch_commits(self):
        assert self.repository.get_commit('1') == Commit(self.repository, '1')


class DemoProxy(RepositoryProxy):
    pass

class describe_repository_proxy:
    def it_is_abstract(self):
        with pytest.raises(TypeError):
            RepositoryProxy()
    
    def it_need_concrete_sublcasses(self):
        with pytest.raises(TypeError):
            DemoProxy()