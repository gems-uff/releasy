import requests
import os
import yaml
import json
import dateutil.parser

from releasy.entity import Issue
from releasy.config import Config

class IssueParser:
    def __init__(self, project):
        self.project = project

    def parse(self):
        if os.path.exists(Config.ISSUES_FILE):
            with open(Config.ISSUES_FILE, 'r') as stream:
                try:
                    issues = yaml.load(stream)
                    for issue in issues:
                        self.project.issues[issue.id] = issue
                except yaml.YAMLError as exc:
                    print(exc)
                    raise


def fetch_issues(url, token=None):
    issues = list()
    url += '?state=all'

    auth = None
    if token:
        url += '&access_token=%s' % token

    has_next = True
    page = 1
    while has_next:
        print('fetching page %d' % page)
        request = requests.get(url + '&page=' + str(page))
        content = json.loads(request.text)

        if content:
            for issue_data in content:
                issue = Issue(issue_data['number'], issue_data['title'])
                issue.author = issue_data['user']['login']
                issue.created = issue_data['created_at']
                if issue_data['closed_at']:
                    issue.closed = issue_data['closed_at']
                for label in issue_data['labels']:
                    issue.labels.append(label["name"])
                issues.append(issue)
                page += 1
            #if page > 1: # todo: handle github limits
            #    has_next = False
        else:
            has_next = False

    return issues

def save_issues(issues, filename):
    with open(filename, 'w') as issues_file:
        yaml.dump(issues, issues_file, default_flow_style=False)

def load_local_issues(file='issues.json'):

    data = None
    try:
        with open(file) as issues_json_file:
            data = json.load(issues_json_file)
    except:
        return None

    issues = list()

    for issue_data in data:
        json_data = json.loads(issue_data)
        issue = Issue(json_data['id'], json_data['subject'])
        issue.labels = json_data['labels']
        issue.closed = None
        if json_data['closed']:
            issue.closed = dateutil.parser.parse(json_data['closed'])
        issue.created = dateutil.parser.parse(json_data['created'])
        issue.author = json_data['author']
        issues.append(issue)

    return issues
