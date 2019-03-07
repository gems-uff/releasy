
from releasy.model import Project, Release, Tag, Commit
from releasy.model_git import GitVcs


def print_commits(project):
    for release in project.releases:
        print(release.name)
        for commit in release.commits:
            print(" - %s" % commit.subject)


def print_release_stat(project):
    print("# releases: %d" % len(project.releases))
    for release in project.releases:
        print("%s\t%s\t%d\t%d\t%d\t%s" % (release.name,
                                  release.typename,
                                  release.commit_count,
                                  release.developer_count,
                                  release.newcommer_count,
                                  release.duration))


project = Project.create("local", ".", GitVcs())
# project = Project.create("local", "../repos/angular", GitVcs())
# project = Project.create("local", "../repos/atom", GitVcs())
# project = Project.create("local", "../repos/mongo", GitVcs())
project = Project.create("local", "../repos/vscode", GitVcs())
# print_commits(project)
print_release_stat(project)
