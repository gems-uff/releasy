
import gitparser
from datetime import datetime
from issue_download import load_local_issues

# issues = load_local_issues('sapos.issues.json')
issues = load_local_issues('brew.issues.json')
history_builder = gitparser.HistoryBuilder(issues)
history = history_builder.build()

def release_prov(release):
    print("  entity(%s, [Timestamp=%s])" % (release.name, release.tag.commit.time.strftime('%Y-%m-%dT%H:%M:%S')))

    for base_release in release.previous:
        print("  entity(%s, , [Timestamp=%s])" % (base_release.name, base_release.tag.commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  wasDerivedFrom(%s,%s)" % (release.name, base_release.name))

    print("  activity(%s-%s, [Label=%s, Timestamp=%s])" % ('implement', release.name, "deliver", release.tag.commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
    print("  wasGeneratedBy(%s,%s-%s,-)" % (release.name, 'implement', release.name))

    for author in release.authors:
        if author.email == 'me@reitermark.us': 
            print("  agent(%s, [Timestamp=%s])" % (author.email, author.first_commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
            print("  activity(%s-%s, [Label=%s, Timestamp=%s])" % ("develop", author.email, "develop", author.first_commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
            print("  wasAssociatedWith(%s-%s,%s,-)" % ("develop", author.email, author.email))

    for issue in release.issues:
        print("  entity(%d, [Timestamp=%s])" % (issue.id, issue.closed.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  used(%s-%s,%d,-)" % ('implement', release.name, issue.id))

        print("  activity(%s-%d, [Label=%s, Timestamp=%s])" % ("implement", issue.id, "implement", issue.closed.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  wasGeneratedBy(%d,%s-%d,-)" % (issue.id, "implement", issue.id))

        for commit in issue.commits:
            if commit.author.email == 'me@reitermark.us': 
                print("\n\n    entity(%s, [Timestamp=%s])" % (commit.hash, commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
                print("    wasGeneratedBy(%s,%s-%s,-)" % (commit.hash, "develop", commit.author.email))
                print("    used(%s-%d,%s,-)" % ("implement", issue.id, commit.hash))

    for commit in release.direct_commits:
        if commit.author.email == 'me@reitermark.us': 
            print("\n\n    entity(%s, [Timestamp=%s])" % (commit.hash, commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
            print("    wasGeneratedBy(%s,%s-%s,-)" % (commit.hash, "develop", commit.author.email))
            print("    used(%s-%s,%s,-)" % ("implement", release.name, commit.hash))


release_name = '4.0.0'
release_name = '4.4.15'
release_name = '4.4.15'
release_name = '1.6.5'
# release_name = '1.5.12'

filter = True
found = False

print('document')
for rls in history.release:
    if not filter or rls.name == release_name:
        release_prov(rls)
        found = True
print('endDocument')
        
if not found:
    print("Release %s not found" % release_name)

