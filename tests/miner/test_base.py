from releasy.miner.base import ReleaseMiner, Repository


class MockRepository(Repository):
    def __init__(self, references) -> None:
        self._references = references

    @property
    def release_refs(self):
        return self._references


class TestReleaseMiner:
    def it_mine_a_repository(self):
        repository = MockRepository(["1.0.0", "1.1.0"])
        release_miner = ReleaseMiner()
        releases = release_miner.mine(repository)

        assert releases[0].name == "1.0.0"
        assert releases[1].name == "1.1.0"
        assert len(releases) == 2
    
    def it_skip_invali_releases(self):
        repository = MockRepository(["1.0.0", "invalid", "1.1.0"])
        release_miner = ReleaseMiner()
        releases = release_miner.mine(repository)

        assert releases[0].name == "1.0.0"
        assert releases[1].name == "1.1.0"
        assert len(releases) == 2
    

