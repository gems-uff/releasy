import sys
import subprocess
import dateutil.parser
import re
import collections

GIT_LOG_FORMAT = collections.OrderedDict([
    ('hash', '%H'),
    ('parent.hash', '%P'),
    ('subject', '%s'),
    ('commiter_date', '%cI'),
    ('refs', '%D'),
    ('author_name', '%aN'),
    ('commiter_name', '%cn'),
    ('author_email', '%aE')
])
# inspired on http://blog.lost-theory.org/post/how-to-parse-git-log-output/
GIT_FORMAT = [v for k, v in GIT_LOG_FORMAT.items()]
GIT_FORMAT = '%x1f'.join(GIT_FORMAT) + '%x1f%x1e'

# Data structures
class Issue():
    def __init__(self, id, subject):
        self.id = id
        self.subject = subject
        self.labels = list()
        self.main_label = None
        self.commits = list()
        self.author = None
        self.created = None
        self.closed = None
        self.released = None
        self.started = None

class Tag():
    def __init__(self, name, commit):
        self.name = name
        self.commit = commit

class Release():
    def __init__(self, tag):
        self.tag = tag
        self.name = tag.name
        self.commits = list()
        self.issues = list()
        self.duration = 0
        self.authors = list()
        self.commiters = list()
        self.direct_commits = list()
        self.previous = list()

# class Feature(object):
#    def __init__(self, id):
#        self.id = id
#        self.commits = list()
#        self.type = 'feature'
#        self.subject = ''

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

class Contributor(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.first_commit = None
    
# History builder - where the magic starts
class HistoryBuilder():
    ''' Build the commit history '''

    def __init__(self, issues = None):
        self.commit = dict()
        self.branch = list()
        self.tag = list()
        self.release = list()
        self.issue = dict()
        self.reg_issues = list()
        self.developers = list()
        self.first_commit = None
        self.last_commit = None
        if issues:
            for issue in issues:
                self.issue[issue.id] = issue
                for label in issue.labels:
                    if re.search(r'^bug', label):
                        issue.main_label = 'bug'
                    if re.search(r'^feat', label):
                        issue.main_label = 'feature'

    def add_commit(self, raw_data): # pylint: disable=E0202
        ''' Record a commit '''
        data = raw_data.split('\x1f')

        author = Contributor(data[5], data[7])

        dev_found = False
        for developer in self.developers:
            if developer.name == author.name:
                dev_found = True

        if not dev_found:
            self.developers.append(author)

        commit_data = {
            'hash': data[0],
            'subject': data[2],
            'parent': list(),
            'commiter': {
                'name': data[6],
                'date': dateutil.parser.parse(data[3])
            },
            'time': dateutil.parser.parse(data[3]),
            'author': author,
            'tags': list(),
            'release': list(),
            'issues': list()
        }


        for parent_hash in data[1].split():
            if parent_hash in self.commit:
                parent = self.commit[parent_hash]
                commit_data['parent'].append(parent)
            else:
                print("missing parent %s" % parent_hash)

        commit = None
        if len(commit_data['parent']) > 1:
            commit = Merge(**commit_data)
        else:
            commit = Commit(**commit_data)
        
        if not author.first_commit:
            author.first_commit = commit 

        if not self.first_commit:
            self.first_commit = commit
        self.last_commit = commit

        self.commit[commit.hash] = commit

        issue_match = re.search(r'#([0-9]+)', commit.subject)
        issue = None
        if issue_match:
            issue_id = int(issue_match.group(1))
            if issue_id in self.issue:
                issue = self.issue[issue_id]
            else:
                issue = Issue(issue_id, "")
                self.issue[issue_id] = issue
            if issue_id not in self.reg_issues:
                self.reg_issues.append(issue_id)

            if not issue.started or issue.started > commit.time:
                issue.started = commit.time
            
            issue.commits.append(commit)
            if issue not in commit.issues:
                commit.issues.append(issue)

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
                    if self.release:
                        release.duration = (release.tag.commit.commiter['date'] - self.release[-1].tag.commit.commiter['date']).days
                    self.release.append(release)

                    find_previous_releases(commit, release)
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

        # print('git log --reverse --all --format="%s"' % GIT_FORMAT)
        log = subprocess.Popen('git log --reverse --all --format="%s"' % GIT_FORMAT,
                               cwd=working_dir ,stdout=subprocess.PIPE, bufsize=1)

        with log.stdout:
            for raw_data in iter(log.stdout.readline, b''):
                self.add_commit(raw_data.decode('utf-8'))

        history = History(self.commit, self.branch, self.tag, self.release, list(self.issue.values()), self.developers)
        return history

class History():
    ''' Store the commit and tag history '''

    def __init__(self, commits, branch, tag, release, issues, developers):
        self.branch = branch
        self.tag = tag
        self.release = release
        self.commits = commits
        self.issues = issues
        self.developers = developers
        self.first_commit = None

def find_previous_releases(commit, release):
    commit_stack = [commit]

    while commit_stack:
        cur_commit = commit_stack.pop()

        cur_commit.release.append(release)

        commit_found = False
        for r_commit in release.commits:
            if r_commit.hash == cur_commit.hash:
                commit_found = True
        if not commit_found:
            release.commits.append(cur_commit)

        # This commit does not implement a feature
        if not cur_commit.issues:
            release.direct_commits.append(cur_commit)

        # Unique authors
        found = False
        for author in release.authors:
            if author.email == cur_commit.author.email:
                found = True
        if not found:
            release.authors.append(cur_commit.author)

        commiter = cur_commit.commiter['name']
        if commiter not in release.commiters:
            release.commiters.append(commiter)

        # Assign issues to release
        for issue in cur_commit.issues:
            if issue not in release.issues:
                release.issues.append(issue)
                if not issue.released or issue.released > release.tag.commit.time:
                    issue.released = release.tag.commit.time

        # Navigate to parent commits
        for parent_commit in cur_commit.parent:
            if not parent_commit.release: # and parent_commit not in release.commits:
                commit_stack.append(parent_commit)

            for previous_release in parent_commit.release:
                new_base_release = True
                for base_release in release.previous:
                    if base_release.name == previous_release.name:
                        new_base_release = False

                if previous_release.name != release.name and new_base_release:
                    release.previous.append(previous_release)
