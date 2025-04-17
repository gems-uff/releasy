from datetime import datetime, timedelta
from typing import Iterable, List
import pytest

from releasy.commit import Commit
from releasy.contributor import Contributor
from releasy.release import Release
from releasy.version import ReleaseVersion
from releasy.old.version_format import ReleaseVersionFormat, SemanticVersioningFormat

@pytest.fixture
def commit() -> Commit:
    return Commit("A")

@pytest.fixture
def commit_a() -> Commit:
    return Commit("A")

@pytest.fixture
def commit_b() -> Commit:
    return Commit("B")

@pytest.fixture
def commit_c() -> Commit:
    return Commit("C")

@pytest.fixture
def commits(commit_a: Commit, commit_b: Commit, commit_c: Commit):
    return set([
        commit_a,
        commit_b,
        commit_c
    ])


@pytest.fixture
def release(version, alice, commit_a) -> Release:
    return Release(
        version=version,
        timestamp=datetime(2024, 1, 1),
        head=commit_a,
        author=alice
    )


@pytest.fixture
def release_a(version_a, alice, commit_a) -> Release:
    return Release(
        version=version_a,
        timestamp=datetime(2024, 1, 1),
        head=commit_a,
        author=alice
    )

@pytest.fixture
def release_b(version_b, alice, commit_b) -> Release:
    return Release(
        version=version_b,
        timestamp=datetime(2024, 1, 1),
        head=commit_b,
        author=alice
    )

@pytest.fixture
def release_c(version_c, alice, commit_c) -> Release:
    return Release(
        version=version_c,
        timestamp=datetime(2024, 1, 1),
        head=commit_c,
        author=alice
    )
