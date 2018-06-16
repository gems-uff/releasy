
import gitparser
import matplotlib.pyplot as plt
import numpy as np
import re

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

release_count = list()
release_number = list()
commit_count = list()
major_version = None
release_duration = list()
xticks = list()
for release in history.release:
    release_count.append(len(release.issues))
    release_number.append(release.tag.name)
    duration = 0
    if release_duration:
        duration += release_duration[-1]
    duration += release.duration
    release_duration.append(duration)
    commit_count.append(len(release.commits))
    version_match = re.match('[0-9]+', release.tag.name)
    if version_match:
        if major_version != version_match.group(0):
            xticks.append(release.tag.name)
            major_version = version_match.group(0)
        else:
            xticks.append('')

plt.plot(np.asarray(release_count))
plt.title('Feature per release')
plt.ylabel('features')
plt.xlabel('versions')
plt.xticks(np.arange(len(xticks)), np.asarray(xticks),rotation=-60)
plt.grid(True)
plt.show()

plt.plot(np.asarray(commit_count))
plt.title('Commit per release')
plt.ylabel('commits')
plt.xlabel('versions')
plt.xticks(np.arange(len(xticks)), np.asarray(xticks),rotation=-60)
plt.grid(True)
plt.show()

plt.plot(np.asarray(release_duration))
plt.title('Release time')
plt.ylabel('days')
plt.xlabel('versions')
plt.xticks(np.arange(len(xticks)), np.asarray(xticks),rotation=-60)
plt.grid(True)
plt.show()
