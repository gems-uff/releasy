import argparse

import releasy.gitparser
from releasy.cli.cli import Cli


class Overview(Cli):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Show project information')
        super().__init__(parser)

    def run(self):
        history_builder = releasy.gitparser.HistoryBuilder(None)
        history = history_builder.build()

        print('Project Overview')
        print(' - %s is the last of %d releases' % (history.release[-1].name, len(history.release)))
        print(' - %d commits made by %d developers' % (len(history.commits), len(history.developers)))
        print(' - %d issues linked' % len(history.issues))

        print('\n\nDevelopers')
        for developer in history.developers:
            print('%s <%s>' % (developer.name, developer.email))
