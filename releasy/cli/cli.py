import argparse

class Cli(object):
    def __init__(self, argv, parser):
        self.argv = argv
        self.parser = parser

    def parse(self):
        self.args = self.parser.parse_args(self.argv)

    def run(self):
        pass
