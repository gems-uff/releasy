import argparse

import releasy.gitparser
from releasy.cli.cli import Cli

class Show(Cli):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Show release information')
        super().__init__(parser)

    def run(self):
        history_builder = releasy.gitparser.HistoryBuilder(None)
        history = history_builder.build()

        release = None
        for rls in history.release:
            if rls.tag.name == self.release:
                release = rls
                break

        if not release:
            print("Release %s not found" % self.release)

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
                    print("  - %d: [%s] %s" % (issue.id, issue.main_label, issue.subject))
                else:
                    print("  - %d: %s" % (issue.id, issue.subject))


