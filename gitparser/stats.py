
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

last = history.release[-1]
print(last.tag.name)
print(len(last.commits))

count = 0
for release in history.release:
    print(release.tag.name, len(release.commits))
    count += len(release.commits)

print(count)
