from datetime import datetime
from typing import Iterable
import pytest

from releasy.change import Change
from releasy.contributor import Contributor
from releasy.release import Release
from releasy.version import ReleaseVersion
from releasy.old.version_format import ReleaseVersionFormat, SemanticVersioningFormat

@pytest.fixture
def change_a() -> Change:
    return Change("A")

@pytest.fixture
def change_b() -> Change:
    return Change("B")

@pytest.fixture
def change_c() -> Change:
    return Change("C")

@pytest.fixture
def changes(change_a: Change, change_b: Change, change_c: Change):
    return set([
        change_a,
        change_b,
        change_c
    ])

@pytest.fixture
def release(
        version: ReleaseVersion, 
        alice: Contributor,
        change_a: Change, 
        changes: Iterable[Change]):
    release = Release(
        version=version, 
        timestamp=datetime(2024, 1, 1),
        head=change_a,
        author=alice
    )
    release.add_changes(changes)
    return release
    
@pytest.fixture
def release_a(version_a: ReleaseVersion, alice: Contributor):
    return Release(
        version=version_a,
        timestamp=datetime(2024, 1, 2),
        head=change_a,
        author=alice
    )

@pytest.fixture
def release_b(version_b: ReleaseVersion, alice: Contributor):
    return Release(
        version=version_b,
        timestamp=datetime(2024, 1, 3),
        head=change_b,
        author=alice
    )

@pytest.fixture
def release_c(version_c: ReleaseVersion, alice: Contributor):
    return Release(
        version=version_c,
        timestamp=datetime(2024, 1, 4),
        head=change_c,
        author=alice
    )
