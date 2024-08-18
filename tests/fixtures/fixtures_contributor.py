import pytest

from releasy.contributor import Contributor


@pytest.fixture
def alice() -> Contributor:
    return Contributor("ALICE")
