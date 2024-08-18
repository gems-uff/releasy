from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from releasy.release import ReleaseVersionFormat

from enum import Enum

from typing import List


class VersionType(Enum):
    MAJOR = 0,
    MINOR = 1,
    PATCH = 2


class ReleaseVersion:
    """
    The release version number. According to the ReleaseFormat, the release
    number can be categorized in the following types:
    - MAJOR
    - MINOR
    - PATCH
    """

    def __init__(self,
            name: str,
            parts: List[str],
            numbers: List[int],
            type: VersionType,
            format: ReleaseVersionFormat) -> None:
        self.name = name
        self.formatted_name = ".".join(parts)
        self.str = parts
        self.number = numbers
        self.type = type
        self.format = format

    def __eq__(self, other: ReleaseVersion):
        if not isinstance(other, ReleaseVersion):
            return False

        for a,b in zip(self.number, other.number):
            if a != b:
                return False

        return True

    def __lt__(self, other: ReleaseVersion):
        if not isinstance(other, ReleaseVersion):
            return False

        for a,b in zip(self.number, other.number):
            if a < b:
                return True

        if a == b:
            return False

        return False

    def __le__(self, other: ReleaseVersion):
        return self < other or self == other

    def __gt__(self, other: ReleaseVersion):
        if not isinstance(other, ReleaseVersion):
            return False

        for a,b in zip(self.number, other.number):
            if a > b:
                return True

        return False

    def __ge__(self, other: ReleaseVersion):
        return self > other or self == other

    def __repr__(self) -> str:
        return self.name