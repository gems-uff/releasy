import pygit2

from releasy.miner2.git import GitReleaseMiner

miner = GitReleaseMiner(pygit2.Repository("."))
releases = miner.mine()

for release in releases:
    print(release.name)


