
from pygit2 import Repository
from pygit2 import GIT_OBJ_COMMIT, GIT_OBJ_TAG

from releasy.model import Project, Release, Tag, Commit
from releasy.model_git import GitCommit, GitTag


def is_release_tag(project, ref):
    """ Check if a tag represents a release """
    if ref.startswith('refs/tags/'):
        tag_name = ref[10:]
        if project.release_pattern.match(tag_name):
            return True
    return False


def is_tracked_commit(commit):
    if commit.release:
        return True
    return False


def track_release(release):
    commit_stack = [ release.head ]
    while len(commit_stack):
        cur_commit = commit_stack.pop()
        cur_commit.release = release
        release.commits.append(cur_commit)
        for parent_commit in cur_commit.parents:
            if is_tracked_commit(parent_commit):
                release.tails.append(cur_commit)
            else:
                commit_stack.append(parent_commit)


project = Project()
path = "."
repo = Repository(path)
commit_dict = {}
releases = []

for ref in repo.references:
    if is_release_tag(project, ref):
        raw_tag = repo.lookup_reference(ref)
        tag = GitTag(repo, raw_tag)
        releases.append(Release(tag))

releases = sorted(releases, key=lambda release: release.time)
for release in releases:
    track_release(release)

for release in releases:
    print(release.name)
    for commit in release.commits:
        print(" - %s" % commit.message)

