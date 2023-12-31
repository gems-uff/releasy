

from datetime import datetime
from releasy.miner.git import GitRepository


class TestGitRepository:
    def it_fetch_release_references(self):
        git = GitRepository(".")
        references = git.release_refs
        references = sorted(references, key=lambda ref: ref.timestamp)
        
        assert references[1].name == '1.0.1'
        assert references[1].description == 'Releasy 1.0.1\n'

        assert references[1].timestamp == \
            datetime.fromisoformat('2018-09-18T00:12:14-03:00')
        assert references[1].developer.startswith('Felipe Curty')
        assert len(references) >= 25
 