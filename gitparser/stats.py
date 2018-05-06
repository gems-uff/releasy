
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

last = history.release[-1]
print(last.tag.name)
print(len(last.commits))

for release in history.release:
    print(release.tag.name, len(release.commits))
