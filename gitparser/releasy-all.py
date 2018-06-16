
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

print('Project Overview')
print(' - %s is the last of %d releases' % (history.release[-1].name, len(history.release)))
print(' - %d commits made by %d developers' % (len(history.commits),len(history.developers)))
print(' - %d issues linked' % len(history.issues))

print('\n\nDevelopers')
for developer in history.developers:
    print('%s <%s>' % (developer.name, developer.email))
