
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

project_start = history_builder.first_commit.time
project_end = history_builder.last_commit.time
time_window = datetime.timedelta(days=1)

cur_time = project_start

backlog_data = []
development_data = []
done_data = []
release_data = []
dates = []

cur_time = project_start
while cur_time < project_end:
    start_frame = cur_time
    end_frame = cur_time + time_window

    backlog_size = 0
    development_size = 0
    done_size = 0
    release_size = 0

    for issue in history.issues:
        if issue.created < end_frame:
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

    backlog_data.append(backlog_size)
    development_data.append(development_size)
    done_data.append(done_size)
    release_data.append(release_size)


    cur_time = end_frame

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator() # every month
yearsFmt = mdates.DateFormatter('%Y')

fig, ax = plt.subplots()
ax.plot(np.asarray(backlog_data))
ax.plot(np.asarray(development_data))
ax.plot(np.asarray(done_data))
ax.plot(np.asarray(release_data))
plt.show()
