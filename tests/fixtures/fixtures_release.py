from datetime import datetime, timedelta
from typing import Iterable, List
import pytest

from releasy.models.commit import Commit
from releasy.models.contributor import Contributor
from releasy.models.release import Release
from releasy.models.version import ReleaseVersion
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
def release(alice, commit_a) -> Release:
    return Release(
        name="r1.0.0",
        timestamp=datetime(2024, 1, 1),
        head=commit_a,
        author=alice,
        message=""
    )


@pytest.fixture
def release_a(alice, commit_a) -> Release:
    return Release(
        name="r1.0.0",
        timestamp=datetime(2024, 1, 1),
        head=commit_a,
        author=alice,
        message=""
    )

@pytest.fixture
def release_b(alice, commit_b) -> Release:
    return Release(
        name="r2.0.0",
        timestamp=datetime(2024, 1, 1),
        head=commit_b,
        author=alice,
        message=""
    )

@pytest.fixture
def release_c(alice, commit_c) -> Release:
    return Release(
        name="r3.0.0",
        timestamp=datetime(2024, 1, 1),
        head=commit_c,
        author=alice,
        message=""
    )
