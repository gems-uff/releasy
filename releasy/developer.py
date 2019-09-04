from __future__ import annotations
from typing import List

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:

from .model import Commit


class Developer:
    """
    Project Contributors

    Attributes:
        login: developer id
        name: developer name
        email: developer e-mail
    """

    def __init__(self):
        self.login = None
        self.name = None
        self.email = None

    def __repr__(self):
        return self.login


class DeveloperRoleTracker():
    """ Track developer roles """
    def __init__(self):
        self.authors = DeveloperTracker()
        self.committers = DeveloperTracker()

    def add_commit(self, commit: Commit):
        self.authors.add(commit.author, commit)
        self.committers.add(commit.committer, commit)


class DeveloperTracker:
    """ Track developers """
    def __init__(self):
        self._developers = {}
#         self._totals = {
#             'commits': 0
#         }

    def add(self, developer: Developer, commit: Commit):
        if developer not in self._developers: 
            self._developers[developer] = []
        self._developers[developer].append(commit)

    def __len__(self):
        return len(self._developers)

    
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
