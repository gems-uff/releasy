
from releasy.model import Tag
from releasy.miner import Miner, Vcs

def test_mine_project_name():
    miner = Miner("../../repos/releasy")
    assert miner._project.name == "releasy"
    
    miner = Miner("releasy")
    assert miner._project.name == "releasy"

    miner = Miner("./releasy")
    assert miner._project.name == "releasy"

def test_mine_simple_project():
    vcs = VcsMock()
    miner = Miner("releasy", vcs)
    project = miner.mine_releases()
    assert len(project.releases) == 4
    assert project.releases[0].version == "1.0.0"
    assert project.releases[1].version == "1.0.1"
    assert project.releases[2].version == "1.1.0"
    assert project.releases[3].version == "2.0.0"

class VcsMock(Vcs):
    def tags(self):
        return [
            Tag("v1.0.0", None),
            Tag("v1.0.1", None),
            Tag("v1.1.0", None),
            Tag("2.0.0", None)
        ]

