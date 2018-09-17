import argparse

import releasy.download
import releasy.gitparser
from releasy.cli.cli import Cli

class Prov(Cli):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Show release information')
        super().__init__(parser)

    def run(self):
        issues = releasy.download.load_local_issues()
        history_builder = releasy.gitparser.HistoryBuilder(issues)
        history = history_builder.build()

        release = None
        for rls in history.release:
            if rls.tag.name == self.release:
                release = rls
                break

        if not release:
            print("Release %s not found" % self.release)

        else:
            release_prov(release)

def release_prov(release):
    print("  entity(%s, [Timestamp=%s])" % (release.name, release.tag.commit.time.strftime('%Y-%m-%dT%H:%M:%S')))

    for base_release in release.previous:
        print("  entity(%s, , [Timestamp=%s])" % (base_release.name, base_release.tag.commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  wasDerivedFrom(%s,%s)" % (release.name, base_release.name))

    print("  activity(%s-%s, [Label=%s, Timestamp=%s])" % ('implement', release.name, "deliver", release.tag.commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
    print("  wasGeneratedBy(%s,%s-%s,-)" % (release.name, 'implement', release.name))

    for author in release.authors:
        print("  agent(%s, [Timestamp=%s])" % (author.email, author.first_commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  activity(%s-%s, [Label=%s, Timestamp=%s])" % ("develop", author.email, "develop", author.first_commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  wasAssociatedWith(%s-%s,%s,-)" % ("develop", author.email, author.email))

    for issue in release.issues:
        print("  entity(%d, [Timestamp=%s])" % (issue.id, issue.closed.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  used(%s-%s,%d,-)" % ('implement', release.name, issue.id))

        print("  activity(%s-%d, [Label=%s, Timestamp=%s])" % ("implement", issue.id, "implement", issue.closed.strftime('%Y-%m-%dT%H:%M:%S')))
        print("  wasGeneratedBy(%d,%s-%d,-)" % (issue.id, "implement", issue.id))

        for commit in issue.commits:
            print("\n\n    entity(%s, [Timestamp=%s])" % (commit.hash, commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
            print("    wasGeneratedBy(%s,%s-%s,-)" % (commit.hash, "develop", commit.author.email))
            print("    used(%s-%d,%s,-)" % ("implement", issue.id, commit.hash))

    for commit in release.direct_commits:
        print("\n\n    entity(%s, [Timestamp=%s])" % (commit.hash, commit.time.strftime('%Y-%m-%dT%H:%M:%S')))
        print("    wasGeneratedBy(%s,%s-%s,-)" % (commit.hash, "develop", commit.author.email))
        print("    used(%s-%s,%s,-)" % ("implement", release.name, commit.hash))
