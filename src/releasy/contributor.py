from __future__ import annotations

from enum import Enum


class Contributor:
    def __init__(self, name: str, email: str = None) -> None:
        self.name = name
        self.email = email
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Contributor):
            return False
        return self.name == other.name and self.email == other.email
