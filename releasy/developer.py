from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from .model import Commit


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


class DeveloperTracker():
    """ Track developers """
    def __init__(self):
        self._developers = []
        self._developers_index = {}
        # self._developers_commits = {}

    def add(self, developer: Developer, commit: Commit):
        new_developer = False
        if developer.login not in self._developers_index:
            self._developers.append(developer)
            self._developers_index[developer.login] = developer
            new_developer = True
        return new_developer

        # if developer.login not in self._developers_index:
        #     self._developers.append(developer)
        #     self._developers_index[developer.login] = len(self._developers)
        #     self._developers_commits[developer.login] = []

        # self._developers_commits[developer.login].append(commit)

    def __len__(self):
        return len(self._developers)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._developers[key]
        else:
            return None
    
#     def list(self):
#         return self._developers.keys()

#     def contains(self, developer):
#         return developer in self._developers

#     def count(self):
#         return len(self.list())

#     def total(self, attribute=None):
#         if not attribute:
#             return self.count()
#         elif attribute in self._totals:
#             return self._totals[attribute]
#         else:
#             return -1

#     def top(self, percent, attribute='commits'):
#         """ Return the top tracked items

#         Params:
#             percent: percentage that the top matches, i.g., 0.8 return the
#                      tracked items responsible for 80% of the total
#         """
#         developers = sorted(self._developers.items(),
#                        key=lambda d:len(d[1]['commits']), 
#                        reverse=True)
#         threshold = min(percent * self._totals['commits'],
#                         self._totals['commits'])
#         amount = 0
#         developers_it = iter(developers)
#         top = DeveloperTracker()
#         while amount < threshold:
#             developer, data = next(developers_it)
#             amount += len(data['commits'])
#             top.add(developer, data['commits'])
#         return top

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
