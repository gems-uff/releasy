
#import releasy

from releasy.miner.vcs.git import GitVcs
from releasy.mine_strategy import TagReleaseMineStrategy, HistoryMineStrategy, TrueReleaseMatcher, TimeMineStrategy

#path = "../../repos2/angular/angular"
# path = "../../repos2/ansible/ansible"
path = "../../repos2/jekyll/jekyll"

vcs = GitVcs(path)
release_matcher = TrueReleaseMatcher()
release_strategy = TagReleaseMineStrategy(vcs, release_matcher)
releases = release_strategy.mine_releases()

print("parsing by history")
history_commit_strategy = HistoryMineStrategy(vcs, releases)
history_release_commits = history_commit_strategy.mine_commits()

print("parsing by time")
time_commit_strategy = TimeMineStrategy(vcs, releases)
time_release_commits = time_commit_strategy.mine_commits()

for release in releases:
    history_set = set(history_release_commits[release.name])
    time_set = set(time_release_commits[release.name])
    
    false_negative = history_set - time_set
    false_positive = time_set - history_set
    true_positive = history_set & time_set
    total = history_set

    if len(true_positive) + len(false_positive) == 0:
        precision = 0
    else:
        precision = len(true_positive) / (len(true_positive) + len(false_positive))

    if (len(true_positive) + len(false_negative)) == 0:
        recall = 0
    else:
        recall = len(true_positive) / (len(true_positive) + len(false_negative))

    if precision+recall == 0:
        fmeasure = 0
    else:
        fmeasure = 2*precision*recall/(precision+recall)

    print(f"f-measure:{fmeasure:1.2f} precision:{precision:1.2f} recall:{recall:1.2f} true_pos:{len(true_positive):4} false_pos:{len(false_positive):4} false_positive:{len(false_negative):4} name:{release.name}")
    #print(f"h:{len(history_release_commits[release.name]):4} t:{len(time_release_commits[release.name]):4} name:{release.name}")

# # Path based
# path = "../../repos2/angular/angular"
# vcs = GitVcs(path)
# release_matcher = TrueReleaseMatcher()
# release_strategy = TagReleaseMineStrategy(vcs, release_matcher)
# releases = release_strategy.mine_releases()

# commit_strategy = HistoryMineStrategy(vcs, releases)
# release_commits = commit_strategy.mine_commits()
# for release in releases:
#     print(f"name: {release.name} count:{len(release_commits[release.name])}")

# # Time based
# path = "../../repos2/angular/angular"
# vcs = GitVcs(path)
# release_matcher = TrueReleaseMatcher()
# release_strategy = TagReleaseMineStrategy(vcs, release_matcher)
# releases = release_strategy.mine_releases()

# commit_strategy = TimeMineStrategy(vcs, releases)
# release_commits = commit_strategy.mine_commits()
# for release in releases:
#     print(f"name: {release.name} count:{len(release_commits[release.name])}")
