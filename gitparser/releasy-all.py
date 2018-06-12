
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

print("Releases: %d" % len(history.release))
print("Commits: %d" % len(history.commits))
print("Last release: %s" % history.release[-1].name)
