
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

release_name = '4.4.15'
release_base = '4.4.14'

for rls in history.release:
    if rls.name == release_name:
        release = rls
        break

if not release:
    print("Release %s not found" % release_name)

else:
    print('document')

    print("  entity(%s)" % release.name)

    print("  entity(%s)" % release_base)
    print("  wasDerivedFrom(%s,%s)" % (release.name, release_base))

    print("  activity(%s-%s)" % ('implement', release.name))
    print("  wasGeneratedBy(%s,%s-%s,-)" % (release.name, 'implement', release.name))

    for author in release.authors:
        print("  agent(%s)" % author.email)
        print("  activity(%s-%s)" % ("develop", author.email))
        print("  wasAssociatedWith(%s-%s,%s,-)" % ("develop", author.email, author.email))

    for issue in release.issues:
        print("  entity(%d)" % issue.id)
        print("  used(%s-%s,%d,-)" % ('implement', release.name, issue.id))

        print("  activity(%s-%d)" % ("implement", issue.id))
        print("  wasGeneratedBy(%d,%s-%d,-)" % (issue.id, "implement", issue.id))

        for commit in issue.commits:
            print("\n\n    entity(%s)" % commit.hash)
            print("    wasGeneratedBy(%s,%s-%s,-)" % (commit.hash, "develop", commit.author.email))
            print("    used(%s-%d,%s,-)" % ("implement", issue.id, commit.hash))

    for commit in release.direct_commits:
        print("\n\n    entity(%s)" % commit.hash)
        print("    wasGeneratedBy(%s,%s-%s,-)" % (commit.hash, "develop", commit.author.email))
        print("    used(%s-%s,%s,-)" % ("implement", release.name, commit.hash))

    print('endDocument')
