from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List

class Developer:
    """
    Project Contributors

    Attributes:
        login: developer id
        name: developer name
        email: developer e-mail
    """

    def __init__(self, login, name, email):
        self.login = login
        self.name = name
        self.email = email

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, obj):
        if isinstance(obj, Developer):
            if self.login == obj.login:
                return True
        return False

    def __repr__(self):
        return self.login


class DeveloperContributionList:
   def __init__(self, developer: Developer):
       pass



class DeveloperRoleTracker():
    """ Track developer roles """
    def __init__(self):
        self.authors = DeveloperTracker()
        self.committers = DeveloperTracker()

    def add_from_commit(self, commit: Commit):
        self.committers.add(commit.committer, commit)
        is_newcomer = self.authors.add(commit.author, commit)
        return is_newcomer


class ReleaseDeveloperRoleTracker(DeveloperRoleTracker):
    def __init__(self):
        super().__init__()
        self.newcomers = DeveloperTracker()
    
    def add_from_commit(self, commit: Commit, is_newcomer=False):
        super().add_from_commit(commit)
        if is_newcomer:        
            self.newcomers.add(commit.author, commit)

    #TODO fix - must pass developers - might be good to have a developercommit class
    def force_newcomer(self, newcomer: Developer):
        self.newcomers.add(newcomer, None)
