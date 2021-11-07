import pytest
from releasy.metamodel import FrequencySet, Commit
from releasy.release import (
    Release, 
    ReleaseSet
)


def test_release_set():
    releases = ReleaseSet()
    releases.add(Release("0", None, None, None))
    releases.add(Release("1", None, None, None))
    assert releases[0].name == "0"
    assert releases[1].name == "1"
    assert releases["1"].name == "1"


def test_release_data():
    releases = ReleaseSet()
    c1 = Commit("a")
    c2 = Commit("b")
    r1 = Release("0", None, None, None)
    r1.commits = [c1]
    r2 = Release("1", None, None, None)
    r2.commits = [c2]
    releases.add(r1)
    releases.add(r2)
    assert c1 in releases[0].commits
    assert c2 in releases[1].commits


def test_frequency_set():
    fset = FrequencySet()
    fset.add("a")
    fset.add("a")
    fset.add("a")
    fset.add("b")
    assert len(fset) == 2
    assert fset.count("a") == 3
    assert fset.count("b") == 1
    assert fset.mode() == "a"
