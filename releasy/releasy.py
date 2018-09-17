import argparse
import sys

import releasy.cli

class Releasy(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Retrieve information from software releases'
        )

        parser.add_argument('release', help='release number')
        parser.add_argument('command', help='subcommand to run')

        args = parser.parse_args(sys.argv[1:3])
        commands = {
            'ls': lambda: releasy.cli.ls.Ls(),
            'show': lambda: releasy.cli.show.Show(),
            'overview': lambda: releasy.cli.overview.Overview(),
            'prov': lambda: releasy.cli.prov.Prov(),
            'download': lambda: releasy.cli.download.Download()
        }

        command = commands.get(args.command, lambda: print("Invalid command"))()
        command.parse(sys.argv[3:])
        command.release = args.release
        command.run()

if __name__ == '__main__':
    Releasy()
