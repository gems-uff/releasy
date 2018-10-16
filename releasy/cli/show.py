import argparse

import releasy.download
import releasy.gitparser
from releasy.cli.base import Project_Cmd

class Show(Project_Cmd):
    def __init__(self, release_name):
        super().__init__()
        self.release_name = release_name

    def run(self):
        release = self.project.release(self.release_name)

        print("Information about release %s" % release.name)
        print("Based on: %s" % ' '.join(rls.name for rls in release.base_releases))
        print("Type: %s" % release.type)
        print("Date: %s" % release.time)
        print("Duration: %s" % release.duration)
        print("Commits: %d" % len(release.commits))

        print("\nDevelopers:")
        for developer in release.developers:
            print("  - %s <%s>" % (developer.name, developer.email))

        print("\nIssues:")
        for issue in release.issues:
            print("  - %d: %s" % (issue.id, issue.subject))


