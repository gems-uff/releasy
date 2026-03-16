
import pytest

from releasy.version_format import ReleaseVersionFormat, SemanticVersioningFormat


@pytest.fixture
def semver_format() -> ReleaseVersionFormat:
    return SemanticVersioningFormat()

@pytest.fixture
def version(semver_format: ReleaseVersionFormat):
    return semver_format.parse("r1.0.0")
    
@pytest.fixture
def version_a(semver_format: ReleaseVersionFormat):
    return semver_format.parse("1.0.0")

@pytest.fixture
def version_b(semver_format: ReleaseVersionFormat):
    return semver_format.parse("1.2.0")

@pytest.fixture
def version_c(semver_format: ReleaseVersionFormat):
    return semver_format.parse("1.2.3")
