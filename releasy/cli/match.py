
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
        parser.add_argument(
            '-t', '--stats',
            help='show match status',
            action='store_true',
            dest='show_stats'
        )
        parser.add_argument(
            '-d', '--detail',
            help='show match status',
            action='store_true',
            dest='show_details'
        )

    def run(self):
        args = self.args
        kwargs = {}
        if self.args.regexp:
            kwargs['regexp'] = args.regexp
        project = ProjectFactory.create(args.path, auto=False, **kwargs)
        if args.save:
            project.save_config()
        print_tag = (not args.show_stats) or (args.release_name)

        matched_count = 0
        unmatched_count = 0
        for tagname in project.tagnames:
            if project.is_release_tag(tagname):
                matched_count += 1
                if (not args.release_name or args.release_name == tagname):
                    if not self.args.inverse and print_tag:
                        if args.show_details:
                            (type, major, minor, patch) = project.release_pattern_search(tagname)
                            print("%s (%s:%s.%s.%s)" % (tagname, type, major, minor, patch))
                        else:
                            print(tagname)
            else:
                unmatched_count += 1
                if self.args.inverse and print_tag:
                    print(tagname)

        if args.show_stats:
            tag_count = matched_count + unmatched_count
            if tag_count > 0:
                matched_percent = 100*matched_count/tag_count
            else:
                matched_percent = 0
            print("M:\t%d\tU:\t%d\tT:\t%d\tP:\t%d" % (matched_count, unmatched_count, tag_count, matched_percent))
