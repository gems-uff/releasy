
import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

for release in history.release:
    print("Release: %s" % release.tag.name)
    print("  Date: %s" % release.tag.commit.commiter['date'])
    print("  Commits: %d" % len(release.commits))
    if release.authors:
        print("  Authors:")
        for author in release.authors:
            print("    - %s" % author['name'])
    if release.features:
        print("  Features:")
        for feature in release.features:
            print("    - %s" % feature.number)
