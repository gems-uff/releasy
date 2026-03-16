import pytest

from releasy.models.contributor import Contributor


@pytest.fixture
def alice() -> Contributor:
    return Contributor("Alice")
