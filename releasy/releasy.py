import argparse
import sys

import cli
#from cli.ls import Ls

class Releasy(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Retrieve information from software releases'
        )

        parser.add_argument('release', help='release number')
        parser.add_argument('command', help='subcommand to run')

        args = parser.parse_args(sys.argv[1:3])
        commands = {
            'ls': lambda: cli.ls.Ls(sys.argv[3:]),
            'show': lambda: cli.show.Show(sys.argv[3:])
        }
        command = commands.get(args.command, lambda: print("Invalid command"))()
        command.parse()
        command.run()

if __name__ == '__main__':
    Releasy()
