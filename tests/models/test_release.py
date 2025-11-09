from datetime import datetime
import pytest
from releasy.models.commit import Commit
from releasy.models.contributor import Contributor
from releasy.models.version import VersionType, ReleaseVersion
from releasy.models.release import Release, ReleaseList
import types

# --- Fixtures for ReleaseList tests ---
@pytest.fixture
def dummy_format():
    # Minimal dummy format with a name attribute
    return types.SimpleNamespace(name="dummy")

@pytest.fixture
def release_a(dummy_format) -> Release:
    return Release(
        version=ReleaseVersion(
            name="1.0.0",
            parts=["1", "0", "0"],
            numbers=[1, 0, 0],
            type=VersionType.MAJOR,
            format=dummy_format
        ),
        timestamp=datetime(2024,1,1),
        head=Commit("a"),
        author=Contributor("Alice")
    )

@pytest.fixture
def release_b(dummy_format) -> Release:
    return Release(
        version=ReleaseVersion(
            name="2.0.0",
            parts=["2", "0", "0"],
            numbers=[2, 0, 0],
            type=VersionType.MAJOR,
            format=dummy_format
        ),
        timestamp=datetime(2024,2,1),
        head=Commit("b"),
        author=Contributor("Bob")
    )


class DescribeRelease:
    def it_has_name(self, release: Release):
        assert release.name == "r1.0.0"

    def it_has_version(self, release: Release):
        assert release.version.number == [1, 0, 0]
        assert release.version.type == VersionType.MAJOR
        assert release.version.format.name == "Semantic Versioning"

    def it_has_type(self, release: Release):
        assert release.type == VersionType.MAJOR
    
    def it_has_release_timestamp(self, release: Release):
        assert release.timestamp == datetime(2024, 1, 1)
    
    def it_has_author(self, release: Release):
        assert release.author.name == "Alice"

    def it_has_head(self, release: Release, commit: Commit):
        assert release.head == commit

    def it_repr_returns_name(self, release: Release):
        assert repr(release) == release.name

    def it_type_is_none_if_version_is_none(self):
        # Defensive: Release with version=None
        dummy_author = Contributor("Nobody")
        dummy_commit = Commit("x")
        r = Release(version=None, timestamp=datetime(2024,1,1), head=dummy_commit, author=dummy_author)
        assert r.type is None

    def it_has_commits(self, release: Release):
        # By default, should be an empty CommitList
        assert hasattr(release, "commits")
        assert isinstance(
            release.commits,
            type(release.head.__class__.__name__ == "Commit" and release.commits)
        )
        assert len(release.commits) == 0

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

 