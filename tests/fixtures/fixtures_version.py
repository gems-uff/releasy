
import pytest

from releasy.version_format import ReleaseVersionFormat, SemanticVersioningFormat


@pytest.fixture
def format():
    return SemanticVersioningFormat()

@pytest.fixture
def version(format: ReleaseVersionFormat):
    return format.parse("r1.0.0")

@pytest.fixture
def version_a(format: ReleaseVersionFormat):
    return format.parse("1.0.0")

@pytest.fixture
def version_b(format: ReleaseVersionFormat):
    return format.parse("1.2.0")

@pytest.fixture
def version_c(format: ReleaseVersionFormat):
    return format.parse("1.2.3")
