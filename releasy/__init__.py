
from .const import *

from releasy.miner.vcs.miner import Miner
from releasy.miner.vcs.git import GitVcs

def mine(path):
    miner = Miner(GitVcs(path))
    project = miner.mine_commits()
    print(RELEASE_TIME)
    return project


# Times
RELEASE_TIME            = 0
START_DEVELOPMENT_TIME  = 1

# lengths
DEVELOPMENT_LENGTH      = 0

# release type
RELEASE_TYPE_MAJOR      = 0b00100
RELEASE_TYPE_MINOR      = 0b00010
RELEASE_TYPE_PATCH      = 0b00001
RELEASE_TYPE_UNKNOWN    = 0b10000
RELEASE_TYPE_PRE        = 0b01000
RELEASE_TYPE_COMMON     = RELEASE_TYPE_MAJOR | RELEASE_TYPE_MINOR | RELEASE_TYPE_PATCH
RELEASE_TYPE_MASK       = 0b11111

RELEASE_TYPE_DUPLICATED = 0b100000
RELEASE_TYPE_ANY        = 0b111111
