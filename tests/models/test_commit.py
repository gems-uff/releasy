import pytest
from releasy.models.commit import Commit, CommitList
from datetime import datetime

@pytest.fixture
def commit_a():
    return Commit("a", datetime(2024,1,1))

@pytest.fixture
def commit_b():
    return Commit("b", datetime(2024,2,1))

class DescribeCommitList:
    def it_supports_index_and_id_access(self, commit_a, commit_b):
        cl = CommitList()
        cl.append(commit_a)
        cl.append(commit_b)
        assert cl[0] == commit_a
        assert cl[1] == commit_b
        assert cl["a"] == commit_a
        assert cl["b"] == commit_b

    def it_iterates_over_commits(self, commit_a, commit_b):
        cl = CommitList([commit_a, commit_b])
        ids = [c.id for c in cl]
        assert ids == ["a", "b"]

    def it_reports_length_and_contains(self, commit_a, commit_b):
        cl = CommitList([commit_a, commit_b])
        assert len(cl) == 2
        assert commit_a in cl
        assert "a" in cl
        assert "notfound" not in cl

    def it_returns_ids(self, commit_a, commit_b):
        cl = CommitList([commit_a, commit_b])
        assert set(cl.ids()) == {"a", "b"}
