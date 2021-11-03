import pytest
from releasy.metamodel import Release, ReleaseSet, ReleaseName, FrequencySet, Commit


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
    r2 = Release("0", None, None, None)
    r2.commits = [c2]
    releases.add(r1)
    releases.add(r2)
    assert c1 in releases[0].commits
    assert c2 in releases[1].commits


def test_release_name():
    release_name = ReleaseName("name", "prefix", "version", "suffix")
    assert release_name == "name"
    assert release_name.value == "name"
    assert release_name.prefix == "prefix"
    assert release_name.version == "version"
    assert release_name.suffix == "suffix"


def test_release_semantic_version():
    release_name = ReleaseName("v1.1.0", "v", "1.1.0", "")
    assert release_name.semantic_version == "1.1.0"
    release_name = ReleaseName("v1.1.1", "v", "1.1.1", "")
    assert release_name.semantic_version == "1.1.1"
    release_name = ReleaseName("v1.0.0", "v", "1.0.0", "")
    assert release_name.semantic_version == "1.0.0"
    release_name = ReleaseName("v1", "v", "1", "")
    assert release_name.semantic_version == "1.0.0"
    release_name = ReleaseName("v2.0", "v", "2.0", "")
    assert release_name.semantic_version == "2.0.0"
    release_name = ReleaseName("v2.1.3.2", "v", "2.1.3.2", "")
    assert release_name.semantic_version == "2.1.3"


def test_release_wo_name():
    with pytest.raises(ValueError):
        release_name = ReleaseName("", "prefix", "version", "suffix")

def test_prefixes():
    releases = ReleaseSet()
    releases.add(Release(ReleaseName("v1.0.0", "v", "1.0.0", ""), None, None, None))
    releases.add(Release(ReleaseName("1.0.1", "", "1.0.1", ""), None, None, None))
    assert len(releases.prefixes) == 2

def test_suffixes():
    releases = ReleaseSet()
    releases.add(Release(ReleaseName("v1.0.0a", "v", "1.0.0", "a"), None, None, None))
    releases.add(Release(ReleaseName("1.0.1", "", "1.0.1", ""), None, None, None))
    assert len(releases.suffixes) == 2


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
