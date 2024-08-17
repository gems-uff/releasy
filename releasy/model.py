from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import re
from typing import List, Set


class Release:
    """
    A Release is a group of changes ready to be delivered to its stakeholders
    """
    def __init__(
            self, 
            name: str = None,
            version: ReleaseVersion = None,
            format: ReleaseFormat = None) -> None:
        self.version = version
        self.name = name 
        if not name and version:
            self.name = ".".join(str(s) for s in version.number)
        self.format = format
        self.previous: Set[Release] = None


    @property
    def type(self) -> ReleaseType:
        if not self.version:
            return None
            
        return self.version.type

    
    @property
    def commits(self) -> Set[Change]:
        pass 

    def __repr__(self) -> str:
        return self.name


class ReleaseVersion:
    """
    The release version number. According to the ReleaseFormat, the release
    number can be categorized in the following types:
    - MAJOR
    - MINOR
    - PATCH
    """

    def __init__(self,
            parts: List[str],
            numbers: List[int],
            type: ReleaseType, 
            format: ReleaseFormat) -> None:
        self.name = ".".join(parts)
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


class ReleaseFormat(ABC):
    """
    A Release format, such as Semantic Versioning. The release format define how
    the release name will be parsed to categorize the release into the following
    categories:
    - MAJOR
    - MINOR
    - PATCH
    """
    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def parse(self, name: str) -> ReleaseVersion:
        """
        Parse the release name according the release format and generate the
        related version
        """
        pass


class SemanticVersioningFormat(ReleaseFormat):
    """
    Implements the Semantic Versioning format 
    """
    part_separator = re.compile(r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)')
    version_separator = re.compile(r'([0-9]+)')
    
    def __init__(self) -> None:
        super().__init__("Semantic Versioning")
        self.part_separator = SemanticVersioningFormat.part_separator
        self.version_separator = SemanticVersioningFormat.version_separator

    def parse(self, name):
        parts = self.part_separator.match(name)

        if not parts.group('version'):
            return None
        version_part = parts.group('version')
        version_str = [
            version
            for version in self.version_separator.findall(version_part)
        ] 
        version_number = [int(version) for version in version_str] 

        match version_number:
            case [_, _, patch] if patch > 0:
                type = ReleaseType.PATCH
            case [_, minor, 0] if minor > 0:
                type = ReleaseType.MINOR
            case _:
                type = ReleaseType.MAJOR

        return ReleaseVersion(version_str, version_number, type, self)


class ReleaseType(Enum):
    MAJOR = 0,
    MINOR = 1,
    PATCH = 2


class Change:
    pass


