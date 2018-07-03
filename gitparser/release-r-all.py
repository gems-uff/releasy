
import gitparser
from issue_download import load_local_issues

# issues = load_issues('https://api.github.com/repos/gems-uff/sapos/issues')
# issues = load_local_issues('sapos.issues.json')
issues = load_local_issues('brew.issues.json')
history_builder = gitparser.HistoryBuilder(issues)
history = history_builder.build()

release = None
for rls in history.release:
    release = rls

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
