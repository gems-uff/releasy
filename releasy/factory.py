
from releasy.model import Project, DeveloperDB
from releasy.model_git import GitVcs


class ProjectFactory():
    @staticmethod
    def create(path, name=None, vcs=None, auto=True, **kwargs):
        if not vcs:
            vcs = GitVcs()
        project = Project(name, path, **kwargs)
        project.vcs = vcs
        project.developer_db = DeveloperDB()
        if auto:
            project.load()
        return project
