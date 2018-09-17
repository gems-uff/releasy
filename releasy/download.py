import requests
import json
import dateutil.parser
from releasy.gitparser import Issue

def load_issues(url):
    issues = list()
    print(url)
    url += '?state=all'

    has_next = True
    page = 1
    while has_next:
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
            if page > 5: # todo: handle github limits
                has_next = False
        else:
            has_next = False

    return issues

def save_issues(url, file='issues.json'):
    issues = load_issues(url)
    issues_json = list()
    for issue in issues:
        issues_json.append(json.dumps(issue.__dict__))

    with open(file, "w") as issues_json_file:
        issues_json_file.write(json.dumps(issues_json, indent=2))

def load_local_issues(file='issues.json'):

    data = None
    with open(file) as issues_json_file:
        data = json.load(issues_json_file)

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

# save_issues('https://api.github.com/repos/gems-uff/sapos/issues', 'sapos.issues.json')
# save_issues('https://api.github.com/repos/Homebrew/brew/issues', 'brew.issues.json')
