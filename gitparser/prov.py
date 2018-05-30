

import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

for release in history.release:
    if release.tag.name == '4.4.15':
        print("entity(%s)" % release.tag.name)
#        print("  Date: %s" % release.tag.commit.commiter['date'])
#        print("  Commits: %d" % len(release.commits))
        if release.authors:
            for author in release.authors:
                print("agent(%s)" % author)
        if release.commiters:
            for commiter in release.commiters:
                pass
                #print("agent(%s)" % commiter)
        if release.features:
            for feature in release.features:
                print("entity(%s)" % feature.number)
