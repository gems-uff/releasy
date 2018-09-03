import argparse

from cli.cli import Cli

class Ls(Cli):
    def __init__(self, argv):
        parser = argparse.ArgumentParser(description='list release data')
        parser.add_argument('command', help='subcommand to run')
        super().__init__(argv, parser)

    def run(self):
        commands = {
            'commit': self.commit
        }    
        command = commands.get(self.args.command, lambda: print("Invalid command"))
        command()

    def commit(self):
        print('commit')
