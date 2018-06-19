
import gitparser
import datetime
from issue_download import load_local_issues
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# issues = load_issues('https://api.github.com/repos/gems-uff/sapos/issues')
issues = load_local_issues('sapos.issues.json')
history_builder = gitparser.HistoryBuilder(issues)
history = history_builder.build()

ignore_issues_without_commit = True

project_start = history_builder.first_commit.time
project_end = history_builder.last_commit.time
time_window = datetime.timedelta(days=1)

cur_time = project_start

backlog_data = []
development_data = []
done_data = []
release_data = []
dates = []
first_issue_date = project_start
first_issue = False
cur_time = project_start
while cur_time < project_end:
    start_frame = cur_time
    end_frame = cur_time + time_window

    backlog_size = 0
    development_size = 0
    done_size = 0
    release_size = 0

    for issue in history.issues:
        if issue.created < end_frame and (issue.commits or not ignore_issues_without_commit):
            backlog_size += 1

            started = False
            closed = False
            released = False
            if issue.started and issue.started < end_frame:
                started = True

            if issue.closed and issue.closed < end_frame:
                closed = True

            if issue.released and issue.released < end_frame:
                released = True
    
            if started or closed or released:
                development_size += 1
            
            if closed or released:
                done_size += 1
            
            if released:
                release_size += 1

    dates.append(cur_time)
    if backlog_size and not first_issue:
        first_issue_date = cur_time
        first_issue = True
    backlog_data.append(backlog_size)
    development_data.append(development_size)
    done_data.append(done_size)
    release_data.append(release_size)


    cur_time = end_frame

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator() # every month
yearsFmt = mdates.DateFormatter('%Y')

labels = ['released', 'done', 'development', 'backlog']
colors = ['#2b83ba', '#abdda4', '#fdae61', '#d7191c']
fig, ax = plt.subplots()

backlog_data = np.asarray(backlog_data)
development_data = np.asarray(development_data)
done_data = np.asarray(done_data)
release_data = np.asarray(release_data)

backlog_data = np.subtract(backlog_data, development_data)
development_data = np.subtract(development_data, done_data)
done_data = np.subtract(done_data, release_data)

y = np.vstack([release_data, done_data, development_data, backlog_data])
ax.stackplot(np.asarray(dates), y, colors=colors, labels=labels)
ax.legend(loc=2)
# ax.stackplot(np.asarray(dates), np.asarray(backlog_data), color='#d7191c')
#ax.stackplot(np.asarray(dates), np.asarray(development_data), color='#fdae61')
#ax.stackplot(np.asarray(dates), np.asarray(done_data), color='#abdda4')
#ax.stackplot(np.asarray(dates), np.asarray(release_data), color='#2b83ba', labels=labels)

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

# format the coords message box
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.grid(True)
ax.set_xlim(first_issue_date,project_end)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

plt.show()


