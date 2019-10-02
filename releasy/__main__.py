import sys

from releasy.miner.vcs.miner import Miner
from releasy.miner.vcs.git import GitVcs

if __name__ == '__main__':
    project_path = sys.argv[1]
    miner = Miner(GitVcs(project_path))
    project = miner.mine_commits()
    print(f"{project.name}")    
