import pytest

from releasy.model import Release, ReleaseFormat, ReleaseVersion, SemanticVersioningFormat

@pytest.fixture
def format():
    return SemanticVersioningFormat()

@pytest.fixture
def version(format: ReleaseFormat):
    return format.parse("1.0.0")

@pytest.fixture
def version_a(format: ReleaseFormat):
    return format.parse("1.0.0")

@pytest.fixture
def version_b(format: ReleaseFormat):
    return format.parse("1.2.0")

@pytest.fixture
def version_c(format: ReleaseFormat):
    return format.parse("1.2.3")

@pytest.fixture
def release(version: ReleaseVersion):
    return Release(version=version)

@pytest.fixture
def release_a(version_a: ReleaseVersion):
    return Release(version=version_a)

@pytest.fixture
def release_b(version_b: ReleaseVersion):
    return Release(version=version_b)

@pytest.fixture
def release_c(version_c: ReleaseVersion):
    return Release(version=version_c)