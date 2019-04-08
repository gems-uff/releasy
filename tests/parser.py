import json

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
        print(json.dumps({
                            'release': str(release),
                            'time': str(release.time),
                            'typename': release.typename,
                            'commits': release.commits.count(),
                            'commits.churn': release.commits.total('churn'),
                            'churn': release.churn,
                            'rework': release.commits.total('churn') - release.churn,
                            'merges': release.commits.total('merges'),
                            'developers': release.developers.count(),
                            'authors': release.developers.authors.count(),
                            'committers': release.developers.committers.count(),
                            'main_developers': release.developers.authors.top(0.8).count(),
                            'newcomers': release.developers.newcomers.count(),
                            'length': str(release.length),
                            'length_group': release.length_group,
                            'length_groupname':release.length_groupname, 
                            'base': str(release.base_releases)
                        }, indent=2))
    #print(project.commits.total('churn'), project.commits.count())
    #print({ 'a':1})

# project = ProjectFactory.create(".", GitVcs())
project = ProjectFactory.create("../../repos/angular", GitVcs())
# project = Project.create("local", "../repos/atom", GitVcs())
# project = Project.create("local", "../repos/mongo", GitVcs())
#project = Project.create("local", "../repos/old/puppet", GitVcs())
# print_commits(project)
print_release_stat(project)
