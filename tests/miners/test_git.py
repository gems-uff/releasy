
from releasy.miners.git import GitMiner

import pytest
import pygit2
import tempfile
import os
import time

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
        commit1_id = repo.create_commit(
            "HEAD",
            author,
            author,
            "first commit",
            tree1,
            []
        )
        repo.create_reference(f"refs/tags/1.0.0", commit1_id)
        
        # Get commit1 timestamp
        commit1 = repo.get(commit1_id)
        commit1_timestamp = commit1.commit_time

        # Second commit
        file2 = os.path.join(repo_dir, "file2.txt")
        with open(file2, "w") as f:
            f.write("second commit\n")
        repo.index.add("file2.txt")
        repo.index.write()
        tree2 = repo.index.write_tree()
        commit2_id = repo.create_commit(
            "HEAD",
            author,
            author,
            "second commit",
            tree2,
            [commit1_id]
        )
        tag2_oid = repo.create_tag(
            "2.0.0",
            commit2_id,
            pygit2.GIT_OBJECT_COMMIT,
            author,
            "Release 2.0.0"
        )

        # Third commit: merge of commit1 and commit2
        # Create a new branch from commit1
        repo.create_reference("refs/heads/feature", commit1_id)
        repo.checkout("refs/heads/feature")
        file3 = os.path.join(repo.workdir, "file3.txt")
        with open(file3, "w") as f:
            f.write("third commit (merge)\n")
        repo.index.add("file3.txt")
        repo.index.write()
        tree3 = repo.index.write_tree()

        author_time = int(time.time()) - 1000  # e.g., 1000 seconds ago
        committer_time = int(time.time()) - 500  # e.g., 500 seconds ago

        committer = pygit2.Signature("Another User", "committer@example.com", committer_time, 0)
        custom_author = pygit2.Signature("Test User", "test@example.com", author_time, 0)
        commit3_id = repo.create_commit(
            "HEAD",
            custom_author,
            committer,
            "third commit (merge)",
            tree3,
            [commit1_id, commit2_id]
        )

        # create a third tag for a non commit object
        blob_oid = repo.create_blob("This is a blob, not a commit.")
        repo.create_tag(
            "blob",
            blob_oid,
            pygit2.GIT_OBJECT_BLOB,
            author,
            "This is a blob tag"
        )
        repo.create_reference("refs/heads/blob2", blob_oid)

        # Get commit1 timestamp
        commit1 = repo.get(commit1_id)
        commit1_timestamp = commit1.commit_time
        
        # Get tag2 timestamp (annotated tag has its own timestamp)
        tag2 = repo.get(tag2_oid)
        tag2_timestamp = tag2.tagger.time
        
        yield repo_dir, \
              str(commit1_id), str(commit2_id), str(commit3_id), \
              commit1_timestamp, tag2_timestamp


class DescribeGitReleaseMiner:
    def it_needs_a_repository_path(self):
        try:
            GitMiner()
        except Exception as e:
            assert isinstance(e, ValueError)
            assert e.args[0] == "Repository path must be provided"

    def it_handles_invalid_repository_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            miner = GitMiner(tmpdir)
            try:
                miner.mine_releases()
            except Exception as e:
                assert isinstance(e, pygit2.GitError)

    class WhenMiningReleases:
        def it_mines_tags(self, temp_git_repo_with_tags):
            (
                repo_dir,
                commit1_oid,
                commit2_oid,
                _,
                commit1_timestamp,
                tag2_timestamp,
            ) = temp_git_repo_with_tags

            miner = GitMiner(repo_dir)
            releases = miner.mine_releases()

            # Should find both tags
            assert set(releases.names()) == {"1.0.0", "2.0.0"}

            # Assert fields for 1.0.0 (lightweight tag)
            assert releases[0].name == "1.0.0"
            assert releases[0].message == "first commit"
            assert releases[0].head.id == str(commit1_oid)
            assert releases[0].author.name == "Test User"
            assert releases[0].author.email == "test@example.com"
            assert releases[0].timestamp.timestamp() == commit1_timestamp

            # Assert fields for 2.0.0 (annotated tag - should use tag timestamp)
            assert releases[1].name == "2.0.0"
            assert releases[1].message == "Release 2.0.0"
            assert releases[1].head.id == str(commit2_oid)
            assert releases[1].author.name == "Test User"
            assert releases[1].author.email == "test@example.com"
            assert releases[1].timestamp.timestamp() == tag2_timestamp

        def it_does_not_mine_non_commit_tags(self, temp_git_repo_with_tags):
            repo_dir, _, _, _, _, _ = temp_git_repo_with_tags
            miner = GitMiner(repo_dir)
            releases = miner.mine_releases()

            names = set(releases.names())
            assert "1.0.1" not in names  # Blob tag should be ignored


        def it_fetches_release_head_parent_relationship_only_after_mining_commits(self, temp_git_repo_with_tags):
            (
                repo_dir,
                _,
                _,
                _,
                _,
                _,
            ) = temp_git_repo_with_tags
            miner = GitMiner(repo_dir)
            releases = miner.mine_releases()
            with pytest.raises(ValueError):
                releases[0].head.parents
    
            miner = GitMiner(repo_dir)
            releases = miner.mine_releases()
            commits = miner.mine_commits()
            releases[0].head.parents

            miner = GitMiner(repo_dir)
            commits = miner.mine_commits()
            releases = miner.mine_releases()
            releases[0].head.parents


    class WhenMiningCommits:
        def it_mines_commits(self, temp_git_repo_with_tags):
            (
                repo_dir,
                commit1_id,
                commit2_id,
                commit3_id,
                _,
                _,
            ) = temp_git_repo_with_tags
            miner = GitMiner(repo_dir)
            commits = miner.mine_commits()

            assert len(commits) == 3
            assert set(commits.ids()) == {
                commit1_id,
                commit2_id,
                commit3_id,
            }
        
        def it_mines_parent_relationships(self, temp_git_repo_with_tags):
            (
                repo_dir,
                commit1_id,
                commit2_id,
                commit3_id,
                _,
                _,
            ) = temp_git_repo_with_tags
            miner = GitMiner(repo_dir)
            commits = miner.mine_commits()

            # commit1 has no parents
            assert not commits[commit1_id].parents

            # commit2 has commit1 as parent
            assert len(commits[commit2_id].parents) == 1
            assert commits[commit2_id]._parents[0].id == commit1_id

            # commit3 is a merge commit with two parents: commit1 and commit2
            assert len(commits[commit3_id].parents) == 2
            parent_ids = set(commits[commit3_id].parents.ids())
            assert parent_ids == {commit1_id, commit2_id}

        def it_differentiates_author_and_committer(self, temp_git_repo_with_tags):
            (
                repo_dir,
                commit1_id,
                _,
                commit3_id,
                _,
                _,
            ) = temp_git_repo_with_tags
            miner = GitMiner(repo_dir)
            commits = miner.mine_commits()

            # commit1: author and committer are the same
            commit1 = commits[commit1_id]
            assert commit1.author.name == "Test User"
            assert commit1.committer.name == "Test User"
            assert commit1.committer == commit1.author

            # commit3: author and committer are different
            commit3 = commits[commit3_id]
            assert commit3.author.name == "Test User"
            assert commit3.committer.name == "Another User"
            assert commit3.committer != commit3.author
