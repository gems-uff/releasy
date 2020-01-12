from datetime import datetime, timedelta
import pytest

from releasy.miner.vcs.miner import Miner

from tests.miner.vcs.mock import DifferentReleaseNameVcsMock

miner = Miner(vcs=DifferentReleaseNameVcsMock(), release_prefixes=["v",""], ignored_suffixes=["Final"])
project = miner.mine_releases()
print(project.release_suffixes)