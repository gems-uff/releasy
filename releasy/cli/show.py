import argparse

import releasy.download
import releasy.gitparser
from releasy.cli.cli import Cli

class Show(Cli):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Show release information')
        super().__init__(parser)

    def run(self):
        print("Information about release %s" % self.release.name)
        print("Based on: %s" % ' '.join(rls.name for rls in self.release.base_releases))
        print("Type: %s" % self.release.type)
        print("Date: %s" % self.release.time)
        print("Duration: %s" % self.release.duration)
        print("Commits: %d" % len(self.release.commits))

        print("\nDevelopers:")
        for developer in self.release.developers:
            print("  - %s <%s>" % (developer.name, developer.email))

        print("\nIssues:")
        for issue in self.release.issues:
            print("  - %d: %s" % (issue.id, issue.subject))


