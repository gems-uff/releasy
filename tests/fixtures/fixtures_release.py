from datetime import datetime, timedelta
from typing import Iterable, List
import pytest

from releasy.commit import CommitSet
from releasy.contributor import Contributor
from releasy.release import Commit, Release
from releasy.version import ReleaseVersion
from releasy.old.version_format import ReleaseVersionFormat, SemanticVersioningFormat

@pytest.fixture
def commit_a() -> Commit:
    return Commit("A")

@pytest.fixture
def commit_b() -> Commit:
    return Commit("B")

@pytest.fixture
def commit_c() -> Commit:
    return Commit("C")

@pytest.fixture
def commits(commit_a: Commit, commit_b: Commit, commit_c: Commit):
    return set([
        commit_a,
        commit_b,
        commit_c
    ])

@pytest.fixture
def release(
        version: ReleaseVersion, 
        alice: Contributor,
        commit_a: Commit, 
        commits: Iterable[Commit],
        prev_release: Release) -> Release:
    release = Release(
        version=version, 
        timestamp=datetime(2024, 1, 3),
        head=commit_a,
        author=alice
    )
    release.set_commits(commits)
    release.add_previous(prev_release)
    return release
    
@pytest.fixture
def release_a(version_a: ReleaseVersion, alice: Contributor, commit_a: Commit):
    return Release(
        version=version_a,
        timestamp=datetime(2024, 1, 1),
        head=commit_a,
        author=alice
    )

@pytest.fixture
def release_b(version_b: ReleaseVersion, alice: Contributor, commit_b):
    return Release(
        version=version_b,
        timestamp=datetime(2024, 1, 3),
        head=commit_b,
        author=alice
    )

@pytest.fixture
def release_c(version_c: ReleaseVersion, alice: Contributor, commit_c):
    return Release(
        version=version_c,
        timestamp=datetime(2024, 1, 5),
        head=commit_c,
        author=alice
    )


@pytest.fixture
def scenario_1(
        semver_format: SemanticVersioningFormat,
        alice: Contributor) -> tuple[CommitSet]:
    commits_history = [
        ("0", [],    [],             [],        [],             alice),
        ("1", ["0"], ["1.0.0"],      [],        [],             alice),
        ("2", ["1"], ["1.1.0"],      ["1.0.0"], [],             alice),
        ("3", ["2"], ["2.0.0-rc.1"], ["1.1.0"], [],             alice),
        ("4", ["3"], ["2.0.0"],      ["1.1.0"], ["2.0.0-rc.1"], alice)
    ]

    commits = CommitSet()
    releases = list()
    timestamp = datetime(2025, 1, 1)
    commit2release = {}
    
    for id, parents_id, release_name, prev_release_names, pre_release_names, author \
            in commits_history:
        parents = [commits[parent_id] for parent_id in parents_id]
        commit = Commit(id, parents, timestamp)
        commits.add(commit)

        for release_name in release_name:
            version = semver_format.parse(release_name)
            release = Release(version, timestamp, commit, author)
            commit2release[commit] = release
            release.set_commits([commit])
            for prev_release_name in prev_release_names:
                release.add_base_release(releases[prev_release_name])
            for pre_release_name in pre_release_names:
                release.add_pre_release(releases[pre_release_name]) 
            releases.add(release)

            release_commits = CommitSet()
            queue = [release.head]
            while queue:
                commit = queue.pop()
                release_commits.add(commit)
                for parent in commit.parents:
                    if parent not in commit2release: 
                        queue.append(parent)
            release.set_commits(release_commits)

        timestamp += timedelta(days=1)

    return releases, commits

@pytest.fixture
def scenario_1_releases(scenario_1) -> List:
    releases, _ = scenario_1
    return releases

@pytest.fixture
def scenario_1_commits(scenario_1) -> CommitSet:
    _, commits = scenario_1
    return commits
