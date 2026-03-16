from datetime import datetime
import pytest
from releasy.models.commit import Commit, CommitList
from releasy.models.contributor import Contributor
from releasy.models.release import Release, ReleaseList

@pytest.fixture
def release_a() -> Release:
    return Release(
        name="1.0.0",
        timestamp=datetime(2024,1,1),
        head=Commit("a"),
        author=Contributor("Alice"),
        message=""
    )

@pytest.fixture
def release_b() -> Release:
    return Release(
        name="2.0.0",
        timestamp=datetime(2024,2,1),
        head=Commit("b"),
        author=Contributor("Bob"),
        message=""
    )


class DescribeRelease:
    def it_has_name(self, release_a: Release):
        assert release_a.name == "1.0.0"

    def it_has_version(self, release_a: Release):
        assert release_a.version is not None
        assert release_a.version.name == "1.0.0"

    def it_has_type(self, release_a: Release):
        assert release_a.type is not None
    
    def it_has_release_timestamp(self, release_a: Release):
        assert release_a.timestamp == datetime(2024, 1, 1)
    
    def it_has_author(self, release_a: Release):
        assert release_a.author.name == "Alice"

    def it_has_head(self, release_a: Release):
        assert isinstance(release_a.head, Commit)

    def it_repr_returns_name(self, release_a: Release):
        assert repr(release_a) == release_a.name

    def it_type_is_none_if_version_is_none(self):
        dummy_author = Contributor("Nobody")
        dummy_commit = Commit("x")
        r = Release(name="dummy", timestamp=datetime(2024,1,1), head=dummy_commit, author=dummy_author, message="")
        assert r.type is None

    def it_has_commits(self, release: Release):
        assert hasattr(release, "commits")
        assert isinstance(release.commits, CommitList)
        assert len(release.commits) == 0

    def it_supports_lazy_loading_commits(self, release: Release):
        c1 = Commit("c1")
        c2 = Commit("c2")

        release.set_commits_loader(lambda: CommitList([c1, c2]))

        loaded = release.commits
        assert len(loaded) == 2
        assert loaded["c1"] == c1
        assert loaded["c2"] == c2

    def it_tracks_previous_and_next(self, release_a: Release, release_b: Release):
        release_b.add_previous(release_a)

        assert release_a in release_b.previous
        assert release_b in release_a.next

    def it_can_add_commits(self, release: Release):
        c1 = Commit("c1")
        c2 = Commit("c2")
        release.commits.append(c1)
        release.commits.append(c2)
        assert release.commits[0] == c1
        assert release.commits[1] == c2
        assert release.commits["c1"] == c1
        assert release.commits["c2"] == c2
        assert len(release.commits) == 2


class DescribeReleaseList:
    def it_exposes_commits_for_each_release(self, release_a, release_b):
        rl = ReleaseList([release_a, release_b])
        c1 = Commit("c1")
        c2 = Commit("c2")
        release_a.commits.append(c1)
        release_b.commits.append(c2)
        assert rl[0].commits[0] == c1
        assert rl[1].commits[0] == c2
        assert rl["1.0.0"].commits[0] == c1
        assert rl["2.0.0"].commits[0] == c2
    def it_supports_index_and_name_access(self, release_a, release_b):
        rl = ReleaseList()
        rl.append(release_a)
        rl.append(release_b)
        assert rl[0] == release_a
        assert rl[1] == release_b
        assert rl["1.0.0"] == release_a
        assert rl["2.0.0"] == release_b

    def it_iterates_over_releases(self, release_a, release_b):
        rl = ReleaseList([release_a, release_b])
        names = [r.name for r in rl]
        assert names == ["1.0.0", "2.0.0"]

    def it_reports_length_and_contains(self, release_a, release_b):
        rl = ReleaseList([release_a, release_b])
        assert len(rl) == 2
        assert release_a in rl
        assert "1.0.0" in rl
        assert "notfound" not in rl

    def it_returns_names(self, release_a, release_b):
        rl = ReleaseList([release_a, release_b])
        assert set(rl.names()) == {"1.0.0", "2.0.0"}

 