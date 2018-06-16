
import gitparser
from issue_download import load_local_issues

# issues = load_issues('https://api.github.com/repos/gems-uff/sapos/issues')
issues = load_local_issues('sapos.issues.json')
history_builder = gitparser.HistoryBuilder(issues)
history = history_builder.build()

release_name = '4.4.15'
# release_name = '1.6.6'

release = None
for rls in history.release:
    if rls.tag.name == release_name:
        release = rls
        break

if not release:
    print("Release %s not found" % release_name)

else:
    print("Information about release %s" % release.tag.name)
    print("Based on: %s" % ' '.join(rls.name for rls in release.previous))
    print("Date: %s" % release.tag.commit.commiter['date'])
    print("Commits: %d" % len(release.commits))

    print("\n\nAuthors:")
    for author in release.authors:
        print("  - %s <%s>" % (author.name, author.email))

    print("\n\nIssues:")
    for issue in release.issues:
        if issue.main_label:
            print("  - [%s] %d: %s" % (issue.main_label, issue.id, issue.subject))
        else:
            print("  - %d: %s" % (issue.id, issue.subject))
