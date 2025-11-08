from releasy.miners.miner import Configuration, Miner
from releasy.miners.json import JsonMiner


class DescribeMinerConfiguration:
    def it_has_a_list_plugins(self):
        config = Configuration(
            plugins=[JsonMiner({})]
        )
        assert len(config.plugins) == 1
        assert isinstance(config.plugins[0], JsonMiner)