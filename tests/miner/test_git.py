

from datetime import datetime
from releasy.miner.git import GitRepository


class DescribeGitRepository:
    def it_fetch_release_references(self):
        git = GitRepository(".")
        references = git.release_refs
        references = sorted(references, key=lambda ref: ref.timestamp)
        
        # Annotated tag
        assert references[1].name == '1.0.1'
        assert references[1].description == 'Releasy 1.0.1\n'
        assert references[1].timestamp == \
            datetime.fromisoformat('2018-09-18T00:12:14-03:00')
        assert references[1].developer.startswith('Felipe Curty')
        assert references[1].change_refs[0].startswith('6cbc46')

        # Tag pointing to a commit
        assert references[18].name == '4.0.1'
        assert references[18].description == 'Fix commit test\n'
        assert references[18].timestamp == \
            datetime.fromisoformat('2022-11-12T18:16:09-03:00')
        assert references[18].developer.startswith('Felipe Curty')
        assert references[18].change_refs[0].startswith('824427')

        assert len(references) >= 25
 