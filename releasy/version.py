
from __future__ import annotations
from abc import ABC, abstractmethod
import re
from typing import List, Tuple



class ReleaseVersion(ABC):
    def __init__(self, numbers: List[int]) -> None:
        self.numbers = numbers


class SimpleReleaseVersion(ReleaseVersion):
    """ The release version is composed by a sequence of numbers and may have a
    prefix and a suffix """
    
    releases_separator = re.compile(
        r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
    )
    number_separator = re.compile(r'([0-9]+)')

    def __init__(self, name) -> None:
        # parts = self.releases_separator.match(name)
        # prefix, version_number, suffix = parts.groups()
        prefix, version_number, suffix = self.releases_separator.findall(name)[0]
        number_parts = self.number_separator.findall(version_number)
        numbers = [int(number) for number in number_parts]
        super().__init__(numbers)
    

class SemanticVersion(SimpleReleaseVersion):
    """ The release version correspond to Semantic Versioning """
    
    def __init__(self, name) -> None:
        super().__init__(name)

    @property
    def major(self):
        return self.numbers[0]

    @property
    def minor(self):
        return self.numbers[1]

    @property
    def patch(self):
        return self.numbers[2]
