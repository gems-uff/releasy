from encodings import aliases

import argparse
import sys

from releasy.config import Config
from releasy.cli.show import Show
from releasy.cli.update import Update

from releasy.cli.ls import Ls
from releasy.cli.overview import Overview
from releasy.cli.prov import Prov
from releasy.cli.download import Download

from releasy.svcparser import GitParser
from releasy.entity import Project
from releasy.issueparser import IssueParser

from releasy.cli.cli import Cli

class Releasy(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Retrieve information from software releases'
        )

        cmd_parser = parser.add_subparsers(
            help='Command',
            dest='cmd'
        )

        parser.add_argument(
            '-w',
            help='working dir'
        )

        cmd_release_parser = argparse.ArgumentParser(add_help=False)
        cmd_release_parser.add_argument(
            'release',
            help='the release version'
        )

        cmd_show_parser = cmd_parser.add_parser(
            'show',
            parents=[cmd_release_parser],
            help='show release information'
        )

        cmd_ls_parser = cmd_parser.add_parser(
            'ls',
            parents=[cmd_release_parser],
            help='list release data'
        )

        cmd_update_parser = cmd_parser.add_parser(
            'update',
            help='Update project issues'
        )
        cmd_update_parser.add_argument(
            '-u','--username',
            metavar='username',
            help='the issue tracker username'
        )
        cmd_update_parser.add_argument(
            '-t',
            metavar='token',
            dest='token',
            help='the OAUTH token'
        )

        args = parser.parse_args()

        commands = {
            'update': lambda: Update(
                token=args.token
            ),
            'show': lambda: Show(
                release_name=args.release
            ),
            'overview': lambda: Overview()
        }

        cmd = commands.get(args.cmd)()
        if args.w:
            cmd.config = Config(base_dir=args.w)
        else:
            cmd.config = Config()

        if 'require_project' in dir(cmd):
            project = Project()
            issueparser = IssueParser(project, config=cmd.config)
            issueparser.parse()
            svcparser = GitParser(project, config=cmd.config)
            svcparser.parse()
            cmd.project = project
        cmd.run()

if __name__ == '__main__':
    releasy = Releasy()
