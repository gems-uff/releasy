
from releasy.factory import ProjectFactory

def test_create():
    pFactory = ProjectFactory()
    project = pFactory.create(".")
    for release in project.releases:
        print(release, release.bugfix_effort)

