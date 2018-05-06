# import os
#import argparse
import sys
import subprocess

# inspired on http://blog.lost-theory.org/post/how-to-parse-git-log-output/
GIT_FORMAT = ['%H', '%P', '%s', '%cI', '%D', '']
GIT_FORMAT = '%x1f'.join(GIT_FORMAT) + '%x1e'

class Tag():
    def __init__(self, name, commit):
        self.name = name
        self.commit = commit

class Release():
    def __init__(self, tag):
        self.tag = tag

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
            'message': data[2],
            'parent': list(),
            'author': {
                'date': data[3]
            }
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

                    # todo: check if tag is a release
                    release = Release(tag)
                    self.release.append(release)
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

        history = History(self.branch, self.tag, self.release)
        return history

class History():
    ''' Store the commit and tag history '''

    def __init__(self, branch, tag, release):
        self.branch = branch
        self.tag = tag
        self.release = release

if __name__ == "__main__":
    hitory_builder = HistoryBuilder()
    history = hitory_builder.build()

    print(len(history.release))
