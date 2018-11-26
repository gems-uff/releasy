
from releasy.factory import ProjectFactory

def test_create():
    pFactory = ProjectFactory()
    project = pFactory.create(".")
    print(project)
