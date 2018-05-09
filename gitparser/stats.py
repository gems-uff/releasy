
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

last = history.release[-1]
print(last.tag.name)
print(len(last.commits))

release_count = 0
feature_count = 0
for release in history.release:
    print(release.tag.name, len(release.commits), len(release.features))
    release_count += len(release.commits)
    feature_count += len(release.features)

print(release_count, feature_count)
feature_count = 0

feature_count = 0
for commit_hash, commit in history.commits.items():
    feature_count += len(commit.features)
print(release_count, feature_count)
