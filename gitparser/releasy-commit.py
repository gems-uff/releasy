
import gitparser
from issue_download import load_local_issues

issues = load_local_issues('brew.issues.json')
history_builder = gitparser.HistoryBuilder(issues)
history = history_builder.build()

release_name = '1.6.5'

release = None
for rls in history.release:
    if rls.tag.name == release_name:
        release = rls
        break

if not release:
    print("Release %s not found" % release_name)

else:
    for commit in release.commits:
        print("%s" % commit.hash)

