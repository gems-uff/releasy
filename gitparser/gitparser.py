# import os
#import argparse
import sys
import subprocess
# from datetime import datetime
import dateutil.parser
import re

# inspired on http://blog.lost-theory.org/post/how-to-parse-git-log-output/
GIT_FORMAT = ['%H', '%P', '%s', '%cI', '%D', '']
GIT_FORMAT = '%x1f'.join(GIT_FORMAT) + '%x1e'

COMMIT_INFO = [
    {'hash': '%H'},
    {'parent.hash': '%P'},
    {'subject': '%s'},
    {'commiter': [
        {'date': '%cI'}
    ]},
    {'refs': '%D'}
]

class Tag():
    def __init__(self, name, commit):
        self.name = name
        self.commit = commit

class Release():
    def __init__(self, tag):
        self.tag = tag
        self.commits = list()
        self.features = list()

class Feature(object):
    def __init__(self, number):
        self.number = number

class Branch():
    def __init__(self, name, commit):
        self.name = name
        self.commit = commit

class Commit(object):
    def __init__(self, **commit):
        self.__dict__.update(commit)

class Merge(Commit):
    def __init__(self, **commit):
        self.__dict__.update(commit)

class HistoryBuilder():
    ''' Build the commit history '''

    def __init__(self):
        self.commit = dict()
        self.branch = list()
        self.tag = list()
        self.release = list()

    def add_commit(self, raw_data): # pylint: disable=E0202
        ''' Record a commit '''
        data = raw_data.split('\x1f')

        commit_data = {
            'hash': data[0],
            'subject': data[2],
            'parent': list(),
            'commiter': {
                'date': dateutil.parser.parse(data[3])
            },
            'tags': list(),
            'release': list(),
            'features': list()
        }

        for parent_hash in data[1].split():
            parent = self.commit[parent_hash]
            commit_data['parent'].append(parent)

        commit = None
        if len(commit_data['parent']) > 1:
            commit = Merge(**commit_data)
        else:
            commit = Commit(**commit_data)

        self.commit[commit.hash] = commit

        feature_match = re.search(r'#([0-9]+)', commit.subject)
        feature = None
        if feature_match:
            feature_number = feature_match.group(1)
            feature = Feature(feature_number)
            if feature not in commit.features:
                commit.features.append(feature)

        if data[4]:
            refs = str(data[4]).split(',')
            for ref in refs:
                ref = ref.strip()
                if ref.startswith('HEAD'):
                    ref = ref.replace('HEAD -> ', '')
                    branch = Branch(ref, commit)
                    self.branch.append(branch)
                elif ref.startswith('tag'):
                    ref = ref.replace('tag: ', '')
                    tag = Tag(ref, commit)
                    self.tag.append(tag)
                    commit.tags.append(tag)

                    # todo: check if tag is a release
                    release = Release(tag)
                    self.release.append(release)

                    move_back_until_release(commit, release)
                else:
                    branch = Branch(ref, commit)
                    self.branch.append(branch)
        

    def build(self):
        ''' Build the whole history '''
        # adapted from [1]
        # [1]: https://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate/17698359#17698359
        if len(sys.argv) > 1:
            working_dir = str(sys.argv[1])
        else:
            working_dir = '.'

        log = subprocess.Popen('git log --reverse --all --format="%s"' % GIT_FORMAT,
                               cwd=working_dir ,stdout=subprocess.PIPE, bufsize=1)

        with log.stdout:
            for raw_data in iter(log.stdout.readline, b''):
                self.add_commit(raw_data.decode('utf-8'))

        history = History(self.commit, self.branch, self.tag, self.release)
        return history

class History():
    ''' Store the commit and tag history '''

    def __init__(self, commits, branch, tag, release):
        self.branch = branch
        self.tag = tag
        self.release = release
        self.commits = commits

def move_back_until_release(commit, release):
    release.commits.append(commit)

    for feature in commit.features:
        if feature not in release.features:
            release.features.append(feature)

    for parent in commit.parent:
        if not parent.tags and parent not in release.commits:
            move_back_until_release(parent, release)
