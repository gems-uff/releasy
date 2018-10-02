import argparse

import releasy.download
import releasy.gitparser
from releasy.cli.cli import Cli

class Show(Cli):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Show release information')
        super().__init__(parser)

    def run(self):
        print("Information about release %s" % self.release.tag.name)
        # print("Based on: %s" % ' '.join(rls.name for rls in self.release.previous))
        print("Date: %s" % self.release.tag.commit.commit_time)
        print("Commits: %d" % len(self.release.commit))

        print("\n\nDevelopers:")
        #for developer in self.release.developers:
        #    print("  - %s <%s>" % (developer.name, developer.email))

        print("\n\nIssues:")
        for issue in self.release.issue.values():
            #if issue.main_label:
            #    print("  - %d: [%s] %s" % (issue.id, issue.main_label, issue.subject))
            #else:
            print("  - %d: %s" % (issue.id, issue.subject))


