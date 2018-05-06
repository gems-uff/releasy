import os
import subprocess

# inspired on http://blog.lost-theory.org/post/how-to-parse-git-log-output/
GIT_FORMAT = ['%H', '%P', '%s', '%cI']
GIT_FORMAT = '%x1f'.join(GIT_FORMAT) + '%x1e'

class History():
    def __init__(self):
        self.history = dict()
        self.last = None

    def commit(self, commit_hash, parent_hashes, commit_message, commit_date):
        parent_commit = list()
        for parent_hash in parent_hashes:
            parent_commit.append(self.history[parent_hash])

        commit = Commit(commit_hash, parent_commit, commit_message, commit_date)
        self.history[commit_hash] = commit
        self.last = commit

    def build(self, commit = None):
        if commit is None:
            commit = self.last

        for parent in commit.parent:
            parent.child.append(commit)
            self.build(parent)
 
class Commit():
    def __init__(self, hash, parent, message, date):
        self.hash = hash
        self.parent = parent
        self.message = message
        self.date = date
        self.child = list()

def main():
    # adapted from https://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate/17698359#17698359
    log = subprocess.Popen('git log --reverse --all --format="%s"' % GIT_FORMAT,
                           stdout=subprocess.PIPE, bufsize=1)

    history = History()
    with log.stdout:
        for log_record in iter(log.stdout.readline, b''):
            log_info = log_record.split(b'\x1f')
            commit_hash = log_info[0]
            parent_hash = log_info[1].split()
            commit_message = log_info[2]
            commit_date = log_info[3]
            history.commit(commit_hash, parent_hash, commit_message, commit_date)
    
    history.build()

main()
