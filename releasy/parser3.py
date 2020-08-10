
#import releasy

from releasy.miner.vcs.git import GitVcs
from releasy.mine_strategy import TagReleaseMineStrategy, HistoryMineStrategy, TrueReleaseMatcher, TimeMineStrategy

# Path based
path = "../../repos2/angular/angular"
vcs = GitVcs(path)
release_matcher = TrueReleaseMatcher()
release_strategy = TagReleaseMineStrategy(vcs, release_matcher)
releases = release_strategy.mine_releases()

commit_strategy = HistoryMineStrategy(vcs, releases)
release_commits = commit_strategy.mine_commits()
for release in releases:
    print(f"name: {release.name} count:{len(release_commits[release.name])}")

# Time based
path = "../../repos2/angular/angular"
vcs = GitVcs(path)
release_matcher = TrueReleaseMatcher()
release_strategy = TagReleaseMineStrategy(vcs, release_matcher)
releases = release_strategy.mine_releases()

commit_strategy = TimeMineStrategy(vcs, releases)
release_commits = commit_strategy.mine_commits()
for release in releases:
    print(f"name: {release.name} count:{len(release_commits[release.name])}")
