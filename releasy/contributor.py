from __future__ import annotations

from enum import Enum


class Contributor:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Contributor):
            return False
        
        return self.name == other.name


# class Person:
#     def __init__(self, name: str) -> None:
#         self.name = name

#     def __eq__(self, other: object) -> bool:
#         if not isinstance(other, Person):
#             return False
        
#         return self.name == other.name

# class Role(Enum):
#     AUTHOR = 0
#     INTEGRATOR = 1
