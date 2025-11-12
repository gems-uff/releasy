
from releasy.miners.release import GitReleaseMiner

import pytest
import pygit2
import tempfile
import os

@pytest.fixture
def temp_git_repo_with_tags():
    with tempfile.TemporaryDirectory() as repo_dir:
        repo = pygit2.init_repository(repo_dir, bare=False)
        author = pygit2.Signature("Test User", "test@example.com")

        # First commit
        file1 = os.path.join(repo_dir, "file1.txt")
        with open(file1, "w") as f:
            f.write("first commit\n")
        repo.index.add("file1.txt")
        repo.index.write()
        tree1 = repo.index.write_tree()
        commit1_oid = repo.create_commit(
            "HEAD",
            author,
            author,
            "first commit",
            tree1,
            []
        )
        repo.create_reference(f"refs/tags/1.0.0", commit1_oid)
        
        # Get commit1 timestamp
        commit1 = repo.get(commit1_oid)
        commit1_timestamp = commit1.commit_time

        # Second commit
        file2 = os.path.join(repo_dir, "file2.txt")
        with open(file2, "w") as f:
            f.write("second commit\n")
        repo.index.add("file2.txt")
        repo.index.write()
        tree2 = repo.index.write_tree()
        commit2_oid = repo.create_commit(
            "HEAD",
            author,
            author,
            "second commit",
            tree2,
            [commit1_oid]
        )
        tag2_oid = repo.create_tag(
            "2.0.0",
            commit2_oid,
            pygit2.GIT_OBJECT_COMMIT,
            author,
            "Release 2.0.0"
        )
        
        # Get commit1 timestamp
        commit1 = repo.get(commit1_oid)
        commit1_timestamp = commit1.commit_time
        
        # Get tag2 timestamp (annotated tag has its own timestamp)
        tag2 = repo.get(tag2_oid)
        tag2_timestamp = tag2.tagger.time
        
        yield repo_dir, commit1_oid, commit2_oid, commit1_timestamp, tag2_timestamp


class DescribeReleaseMiner:
    def it_mines_tags(self, temp_git_repo_with_tags):
        repo_dir, commit1_oid, commit2_oid, commit1_timestamp, tag2_timestamp = (
            temp_git_repo_with_tags
        )
        miner = GitReleaseMiner(repo_dir)
        releases = miner.mine()

        # Should find both tags
        names = set(releases.names)
        assert names == {"1.0.0", "2.0.0"}

        # Assert fields for 1.0.0 (lightweight tag)
        assert releases[0].name == "1.0.0"
        assert releases[0].message == "first commit"
        assert releases[0].head == str(commit1_oid)
        assert releases[0].author.name == "Test User"
        assert releases[0].author.email == "test@example.com"
        assert releases[0].timestamp.timestamp() == commit1_timestamp

        # Assert fields for 2.0.0 (annotated tag - should use tag timestamp)
        assert releases[1].name == "2.0.0"
        assert releases[1].message == "Release 2.0.0"
        assert releases[1].head == str(commit2_oid)
        assert releases[1].author.name == "Test User"
        assert releases[1].author.email == "test@example.com"
        assert releases[1].timestamp.timestamp() == tag2_timestamp

    def it_needs_a_repository_path(self):
        miner = GitReleaseMiner()
        try:
            miner.mine()
        except Exception as e:
            assert isinstance(e, ValueError)
            assert e.args[0] == "Repository path must be provided"

    def it_handles_invalid_repository_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            miner = GitReleaseMiner(tmpdir)
            try:
                miner.mine()
            except Exception as e:
                assert isinstance(e, pygit2.GitError)



