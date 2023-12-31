

from releasy.miner.git import GitRepository


class TestGitRepository:
    def it_fetch_release_references(self):
        git = GitRepository(".")
        references = git.release_refs
        references = sorted(references, key=lambda ref: ref.timestamp)
        
        assert references[0].name == "1.0.0"
        assert references[1].name == "1.0.1"
        assert len(references) >= 25
 