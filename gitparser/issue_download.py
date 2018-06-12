import requests
import json
from gitparser import Issue

def load_issues(url):
    issues = []
    url += '?state=all'

    has_next = True
    page = 1
    while has_next:
        request = requests.get(url + '&page=' + str(page))
        content = json.loads(request.text)

        if len(content):
            for issue_data in content:
                issue = Issue(issue_data['number'], issue_data['title'])
                for label in issue_data['labels']:
                    issue.labels.append(label["name"])                
                issues.append(issue)
            page += 1
        else:
            has_next = False
        
        has_next = False

    return issues

