import os
import subprocess

# inspired on http://blog.lost-theory.org/post/how-to-parse-git-log-output/
GIT_FORMAT = ['%H', '%P', '%cI']
GIT_FORMAT = '%x1f'.join(GIT_FORMAT) + '%x1e'

def main():
    # adapted from https://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate/17698359#17698359
    log = subprocess.Popen('git log --format="%s"' % GIT_FORMAT, stdout=subprocess.PIPE, bufsize=1)
    with log.stdout:
        for log_record in iter(log.stdout.readline, b''):
            log_info = log_record.split(b'\x1f')
            commit_hash = log_info[0]
            parent_hash = log_info[1].split()
            commit_date = log_info[2]
            print(commit_hash, parent_hash, commit_date)

main()
