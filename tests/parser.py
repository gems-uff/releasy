
from releasy.model import Project, Release, Tag, Commit
from releasy.model_git import GitVcs
from releasy.factory import ProjectFactory

def print_commits(project):
    for release in project.releases:
        print(release.name)
        for commit in release.commits:
            print(" - %s" % commit.subject)


def print_release_stat(project):
    print("# releases: %d" % len(project.releases))
    for release in project.releases:
        print("%-15s %s %d %d %d %s %d %d %s %d %s" % (release.name,
                                  release.typename,
                                  release.commits.count(),
                                  release.developers.authors.count(),
                                  release.developers.committers.count(),
                                  release.developers.count(),
                                  release.developers.newcomers.count(),
                                  release.commits.total('churn'),
                                  release.length,
                                  release.length_group,
                                  release.length_groupname))
    print(project.commits.total('churn'), project.commits.count())


project = ProjectFactory.create(".", GitVcs())
#project = ProjectFactory.create("../../repos/angular", GitVcs())
# project = Project.create("local", "../repos/atom", GitVcs())
# project = Project.create("local", "../repos/mongo", GitVcs())
#project = Project.create("local", "../repos/old/puppet", GitVcs())
# print_commits(project)
print_release_stat(project)
