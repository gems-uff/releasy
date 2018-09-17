import argparse

import releasy.gitparser
import releasy.download
from releasy.cli.cli import Cli

class Download(Cli):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Show release information')
        parser.add_argument('url', help='issue tracker url')
        super().__init__(parser)

    def run(self):
        url = super().getArgs().url
        releasy.download.save_issues(url)

