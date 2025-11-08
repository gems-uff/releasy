from abc import ABC, abstractmethod
import re

from releasy.models.version import VersionType, ReleaseVersion


class ReleaseVersionFormat(ABC):
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


class SemanticVersioningFormat(ReleaseVersionFormat):
    """
    Implements the Semantic Versioning format 
    """
    part_separator = re.compile(r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)')
    version_separator = re.compile(r'([0-9]+)')
    
    def __init__(self) -> None:
        super().__init__("Semantic Versioning")
        self.part_separator = SemanticVersioningFormat.part_separator
        self.version_separator = SemanticVersioningFormat.version_separator

    def parse(self, name: str) -> ReleaseVersion:
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
                type = VersionType.PATCH
            case [_, minor, 0] if minor > 0:
                type = VersionType.MINOR
            case _:
                type = VersionType.MAJOR

        return ReleaseVersion(name, version_str, version_number, type, self)