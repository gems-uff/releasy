import subprocess
import dateutil.parser
import re
import collections

from releasy.entity import Commit
from releasy.entity import Tag
from releasy.entity import Issue
from releasy.entity import Developer
from releasy.entity import Release

class SvcParser():
    def __init__(self, project):
        self.project = project

    def get_developer(self, email, name):
        if email not in self.project.developer.keys():
            self.project.developer[email] = Developer(email, name)
        return self.project.developer.get(email)

    def get_commit(self, hash):
        if hash not in self.project.release['ALL'].commit.keys():
            self.project.release['ALL'].commit[hash] = Commit(hash)
        return self.project.release['ALL'].commit[hash]

    def get_tag(self, ref):
        if ref not in self.project.tag.keys():
            self.project.tag[ref] = Tag(ref)
        return self.project.tag[ref]

    def get_issue(self, issue_id):
        if issue_id not in self.project.release['ALL'].issue.keys():
            self.project.release['ALL'].issue[issue_id] = Issue(issue_id)
        return self.project.release['ALL'].issue[issue_id]

    def get_release(self, tag):
        if tag.name not in self.project.release.keys():
            self.project.release[tag.name] = Release(tag)
        return self.project.release[tag.name]

    def add_commit(self, commit, release=None):
        self.project.release['ALL'].commit[commit.hash] = commit

class GitParser(SvcParser):
    GIT_LOG_FORMAT = collections.OrderedDict([
        ('hash', '%H'),
        ('parent.hash', '%P'),
        ('subject', '%s'),
        ('refs', '%D'),
        ('commiter_email', '%cE'),
        ('commiter_name', '%cn'),
        ('commiter_date', '%cI'),
        ('author_email', '%aE'),
        ('author_name', '%aN'),
        ('author_date', '%aI')
    ])
    # inspired on http://blog.lost-theory.org/post/how-to-parse-git-log-output/
    GIT_FORMAT = [v for k, v in GIT_LOG_FORMAT.items()]
    GIT_FORMAT = '%x1f'.join(GIT_FORMAT) + '%x1f%x1e'
    
    def __init__(self, project):
        super().__init__(project)

    def parse(self):
        print('git log --all --format="%s"' % GitParser.GIT_FORMAT)
        log = subprocess.Popen('git log --all --format="%s"' % GitParser.GIT_FORMAT,
                               stdout=subprocess.PIPE, bufsize=1, shell=True)

        with log.stdout:
            for raw_data in iter(log.stdout.readline, b''):
                data = raw_data.decode('utf-8').split('\x1f')
                self.parse_commit(data)

        self.parse_releases()

    def parse_commit(self, data):
        commit = self.get_commit(data[0])
        commit.subject = data[2]

        parents = []
        for parent_hash in data[1].split():
            parent = self.get_commit(parent_hash)
            if not parent:
                print("missing parent %s" % parent_hash)
            parents.append(parent)
        commit.parent = parents

        commit.commiter = self.get_developer(data[4], data[5])
        commit.commit_time = dateutil.parser.parse(data[6])
        commit.developer = self.get_developer(data[7], data[8])
        commit.development_time = dateutil.parser.parse(data[9])

        # tags
        if data[3]:
            refs = str(data[3]).split(',')
            for ref in refs:
                ref = ref.strip()
                if ref.startswith('tag'):
                    ref = ref.replace('tag: ', '')
                    tag = self.get_tag(ref)
                    tag.commit = commit
                    commit.tag.append(tag)

                    # todo if tag is release
                    if True:
                        release = self.get_release(tag) #todo rename to build release
                        commit.release.append(release)

        self.add_commit(commit)

        # issues
        issue_match = re.search(r'#([0-9]+)', commit.subject)
        issue = None
        if issue_match:
            issue_id = int(issue_match.group(1))
            issue = self.get_issue(issue_id)
            if issue not in commit.issue:
                commit.issue.append(issue)

    def parse_releases(self):
        for ref,release in self.project.release.items():
            if isinstance(release, Release):
                add_commit_to_release(release.tag.commit, release)


def add_commit_to_release(commit, release):
    commit_stack = [commit]

    while commit_stack:
        cur_commit = commit_stack.pop()

        release.get_commit()[cur_commit.hash] = cur_commit
        if release not in cur_commit.release:
            cur_commit.release.append(release)

        # add developers to release
        # add issues to release
        if commit.issue:
            for issue in commit.issue:
                release.issue[issue.id] = issue

        # Navigate to parent commits
        #todo releases that point to same commit
        for parent_commit in cur_commit.parent:
            if not parent_commit.release: # and parent_commit not in release.commits:
                commit_stack.append(parent_commit)

            # add base release
