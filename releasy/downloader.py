import sys
import re
import requests
import json
import codecs
import traceback

from pygit2 import Repository
from releasy.config import Config

repo_path = sys.argv[1]
page = int(sys.argv[2])
token = None
if len(sys.argv) == 4:
    token = sys.argv[3]

repo = Repository(repo_path)

origin = repo.remotes['origin']
origin_url = origin.url

raw_issues = []
config = Config(repo_path)
if page > 1:
    with open(config.issues_file, 'rb') as stream:
        raw_issues = json.load(stream)

if re.search("github",origin_url):
    api_url = re.sub("https?://github.com/([a-zA-Z0-9_]*)/([a-zA-Z0-9_]+).git",
                     "https://api.github.com/repos/\g<1>/\g<2>/issues",
                     origin_url)

    issues = list()
    api_url += '?state=all&per_page=100'

    if token:
        api_url += '&access_token=%s' % token

    try:
        has_next = True
        while has_next:
            print('fetching page %d' % page)
            request = requests.get(api_url + '&page=' + str(page))
            content = json.loads(request.text)

            raw_issues_page = []
            if content:
                for data in content:
                    issue = {
                        'id': data['number'],
                        'subject': data['title'],
                        'created': data['created_at'],
                        'author': data['user']['login'],
                        'labels': []
                    }
                    if 'closed_at' in data:
                        issue['closed'] = data['closed_at']
                    if 'updated_at' in data:
                        issue['updated'] = data['updated_at']
                    for label in data['labels']:
                        issue['labels'].append(label["name"])
                    if 'pull_request' in data:
                        issue['pull_request'] = True
                    raw_issues_page.append(issue)

                page += 1
                raw_issues += raw_issues_page
            else:
                has_next = False
    except Exception as e:
        traceback.print_exc()
    finally:
        with open(config.issues_file, 'wb') as outfile:
            json.dump(raw_issues, codecs.getwriter('utf-8')(outfile), ensure_ascii=False)
