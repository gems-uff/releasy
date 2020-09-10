import pytest
from releasy.data import Release, ReleaseSet, Commit, ReleaseName

def test_release_set():
    releases = ReleaseSet()
    releases.add(Release("0", None, None, None), None)
    releases.add(Release("1", None, None, None), None)
    assert releases[0].name == "0"
    assert releases[1].name == "1"
    assert releases["1"].name == "1"
  

def test_release_data():
    releases = ReleaseSet()
    c1 = Commit("a")
    c2 = Commit("b")
    releases.add(Release("0", None, None, None), [c1])
    releases.add(Release("1", None, None, None), [c2])
    assert c1 in releases[0].commits
    assert c2 in releases[1].commits


def test_release_name():
    release_name = ReleaseName("name", "prefix", "version", "suffix")
    assert str(release_name) == "name"
    assert release_name.value == "name"
    assert release_name.prefix == "prefix"
    assert release_name.version == "version"
    assert release_name.suffix == "suffix"


def test_release_wo_name():
    with pytest.raises(ValueError):
        release_name = ReleaseName("", "prefix", "version", "suffix")

