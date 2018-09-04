import argparse

class Cli(object):
    '''Command Line Interface superclass'''
    def __init__(self, parser):
        self.parser = parser

    def parse(self, argv):
        self.args = self.parser.parse_args(argv)

    def run(self):
        pass
