

import gitparser

history_builder = gitparser.HistoryBuilder()
history = history_builder.build()

print('document')
for release in history.release:
    if release.tag.name == '4.4.15':
        print("  entity(%s)" % release.tag.name)
        print("  activity(%s)" % 'implement')
        print("  wasGeneratedBy(%s, %s, -)" % (release.tag.name, 'develop'))
        if release.authors:
            for author in release.authors:
                print("  agent(%s)" % author)
                print("  wasAssociatedWith(%s, %s, -)" % ('develop', author))
        if release.commiters:
            for commiter in release.commiters:
                pass
                #print("agent(%s)" % commiter)
        #print("  activity(%s)" % 'composed')
        #print("  wasGeneratedBy(%s, %s, -)" % (release.tag.name, 'authored'))
        if release.features:
            for feature in release.features:
                print("  entity(%s)" % feature.number)
                print("  used(%s,%s, -)" % ('authored', feature.number))

print('endDocument')
