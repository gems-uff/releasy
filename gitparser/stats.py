
import gitparser

hitory_builder = gitparser.HistoryBuilder()
history = hitory_builder.build()

last = history.release[-1]
print(last.tag.name)
print(len(last.commits))
