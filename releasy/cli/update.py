import getpass
import os

from releasy.cli.base import Cmd
from releasy.config import Config
from releasy.issueparser import fetch_issues
from releasy.issueparser import save_issues

class Update(Cmd):
    def __init__(self, token=None):
        self.token = token

    def run(self):
        url = self.config.prop['issue_tracker']['url']
        issues = fetch_issues(url, self.token)
        if issues:
            #todo fix
            save_issues(issues, filename=self.config.issues_file)
