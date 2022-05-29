from typing import Set
import pytest
from releasy.repository import Commit, Repository, Tag
from .mock_repository import MockRepositoryProxy


class describe_tag:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = Repository(MockRepositoryProxy())

    def it_has_repository(self):
        tag = Tag(self.repository, '1.0.0')
        assert tag.repository

    def it_has_name(self):
        tag = Tag(self.repository, '1.0.0')
        assert tag.name == '1.0.0'

    def it_has_commit(self):
        tag = Tag(self.repository, '1.0.0', Commit(self.repository, '1'))
        assert Commit(self.repository, '1') == tag.commit


class describe_commit:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = Repository(MockRepositoryProxy())

    def it_has_repository(self):
        commit = Commit(self.repository, '1')
        assert commit.repository

    def it_has_id(self):
        commit = Commit(self.repository, '1')
        assert commit.id == '1'

    def it_has_parents(self):
        commit = Commit(self.repository, '14')
        assert Commit(self.repository, '12') in commit.parents
        assert Commit(self.repository, '13') in commit.parents


class describe_repository:
    @pytest.fixture(autouse=True)
    def init(self):
        self.repository = Repository(MockRepositoryProxy())

    def it_fetch_tags(self):
        tags = self.repository.get_tags()
        assert len(tags) == 11
        assert Tag(self.repository, '1.1.0') in tags