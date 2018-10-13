import argparse
import sys

from releasy.config import Config
from releasy.cli.ls import Ls
from releasy.cli.show import Show
from releasy.cli.overview import Overview
from releasy.cli.prov import Prov
from releasy.cli.download import Download

from releasy.svcparser import GitParser
from releasy.entity import Project

class Releasy(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Retrieve information from software releases'
        )

        parser.add_argument('release', help='release number')
        parser.add_argument('command', help='subcommand to run')

        args = parser.parse_args(sys.argv[1:3])
        commands = {
            'ls': lambda: Ls(),
            'show': lambda: Show(),
            'overview': lambda: Overview(),
            'prov': lambda: Prov(),
            'download': lambda: Download()
        }

        command = commands.get(args.command, lambda: print("Invalid command"))()
        command.parse(sys.argv[3:])

        config = Config()

        project = Project()
        svcparser = GitParser(project)
        svcparser.parse()

        if "issue_tracker" in config.prop:
            pass

        release_ref = args.release
        release = None
        if project.contains_release(release_ref):
            release = project.release(release_ref)

        command.release = release
        command.run()

if __name__ == '__main__':
    Releasy()
