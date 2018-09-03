import argparse

import gitparser
from cli.cli import Cli

class Show(Cli):
    def __init__(self, argv):
        parser = argparse.ArgumentParser(description='Show release information')
        super().__init__(argv, parser)

    def run(self):
        issues = []
        history_builder = gitparser.HistoryBuilder(issues)
        history = history_builder.build()

