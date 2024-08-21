

from releasy.change import Change
from releasy.repository import Repository

class MockRepository(Repository):
    def __init__(self, releases, commits) -> None:
        super().__init__()


A = Change("A")
B = Change("B", [A])
C = Change("C", [B])
D = Change("D", [B])
E = Change("E", [C, D])


