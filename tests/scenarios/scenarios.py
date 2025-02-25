

from releasy.commit import Commit
from releasy.repository import Repository

class MockRepository(Repository):
    def __init__(self, releases, commits) -> None:
        super().__init__()


A = Commit("A")
B = Commit("B", [A])
C = Commit("C", [B])
D = Commit("D", [B])
E = Commit("E", [C, D])


