
import argparse

from releasy.cli.base import BaseCli
from releasy.model_git import Project
from releasy.factory import ProjectFactory

class Match(BaseCli):
    """ Test release name matches of a project """
    def __init__(self):
        super().__init__()
        self.help = 'Test release name matches of a project'

    def build_parser(self, parser):
        parser.add_argument(
            '-e',
            metavar='regexp',
            help='show unmatched releases',
            dest='regexp'
        )
        parser.add_argument(
            '-v',
            help='show unmatched releases',
            action = 'store_true',
            dest='inverse'
        )
        parser.add_argument(
            '-s',
            help='save regexp to project configuration',
            action = 'store_true',
            dest='save'
        )
        parser.add_argument(
            'path',
            help='project path',
            nargs='?',
            default='.'
        )

    def run(self):
        kwargs = {}
        if self.args.regexp:
            kwargs['regexp'] = self.args.regexp
        project = ProjectFactory.create(self.args.path, auto=False, **kwargs)

        for tagname in project.tagnames:
            if project.is_release_tag(tagname):
                if not self.args.inverse:
                    print(tagname)
            else:
                if self.args.inverse:
                    print(tagname)
