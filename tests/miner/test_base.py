from releasy.miner.base import ReleaseMiner, Repository


class MockRepository(Repository):
    @property
    def release_refs(self):
        return ["1.0.0", "1.1.0", "1.1.1", "2.0.0"]


class TestReleaseMiner:

    class WithSimpleRepo:
    
        def it_mine_a_repository(self):
            repository = MockRepository()
            release_miner = ReleaseMiner()
            releases = release_miner.mine(repository)

            assert len(releases) == 4
        
        

