
import argparse

from releasy.cli.base import BaseCli


class Ls(BaseCli):
    """ Show release informatioin """
    def run(self):
        args = self.args
        print(args.release_name)

    def p(self):
        pass
              
