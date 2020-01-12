from datetime import datetime, timedelta
import pytest

from releasy.miner.vcs.miner import Miner

from tests.miner.vcs.mock import VcsMock

miner = Miner(vcs=VcsMock())
project = miner.mine_releases()
assert not project.releases[0].is_duplicated()
assert not project.releases[1].is_duplicated()
assert not project.releases[2].is_duplicated()
assert not project.releases[3].is_duplicated()
assert not project.releases[4].is_duplicated()
assert not project.releases[5].is_duplicated()
print(project.releases[6], project.releases[6].original)
#assert project.releases[6].is_duplicated()
assert not project.releases[7].is_duplicated()
assert project.releases[6].original == project.releases[5]
