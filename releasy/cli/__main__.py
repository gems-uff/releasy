"""
Releasy Command Line Interface
"""
import argparse

from releasy.cli.match import Match


class ReleasyCli:
    """ Dispatcher for subcommands """

    def __init__(self):
        parser = argparse.ArgumentParser(prog='releasy')
        commands_parser = parser.add_subparsers(
            help='Command',
            dest='cmd'
        )

        commands = {
            'match': Match()
        }

        for command, clazz in commands.items():
            command_parser = commands_parser.add_parser(command, help=clazz.help)
            clazz.build_parser(command_parser)

        args = parser.parse_args()
        if args.cmd in commands.keys():
            commands[args.cmd].args = args
            commands[args.cmd].run()


if __name__ == '__main__':
    releasy = ReleasyCli()
