from datetime import datetime
import pytest

from releasy.contributor import Contributor
from releasy.release import Release
from releasy.version import ReleaseVersion
from releasy.version_format import ReleaseVersionFormat, SemanticVersioningFormat


@pytest.fixture
def release(version: ReleaseVersion, alice: Contributor):
    return Release(
        version=version, 
        timestamp=datetime(2024, 1, 1),
        author=alice
    )
    
@pytest.fixture
def release_a(version_a: ReleaseVersion, alice: Contributor):
    return Release(
        version=version_a,
        timestamp=datetime(2024, 1, 2),
        author=alice
    )

@pytest.fixture
def release_b(version_b: ReleaseVersion, alice: Contributor):
    return Release(
        version=version_b,
        timestamp=datetime(2024, 1, 3),
        author=alice
    )

@pytest.fixture
def release_c(version_c: ReleaseVersion, alice: Contributor):
    return Release(
        version=version_c,
        timestamp=datetime(2024, 1, 4),
        author=alice
    )
