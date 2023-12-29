
from __future__ import annotations
from abc import ABC, abstractmethod
import re
from typing import Tuple

class ReleaseVersioningSchema(ABC):
    @abstractmethod
    def parse(self, name: str) -> Tuple[str, ReleaseVersion]:
        pass


class SemanticVersioningSchema(ReleaseVersioningSchema):
    def parse(self, name: str) -> Tuple[str, ReleaseVersion]:
       version = SemanticVersioning(name) 
       return version


class SimpleVersioningSchema(ReleaseVersioningSchema):
    def parse(self, name: str) -> Tuple[str, ReleaseVersion]:
        return super().parse(name)

class ReleaseVersion(ABC):
    pass

class SemanticVersioning(ReleaseVersion):
    def __init__(self, name) -> None:
        self.prefix = ''
        self.suffix = ''
        
        if not separator:
            separator = re.compile(
                r'(?P<prefix>(?:[^\s,]*?)(?=(?:[0-9]+[\._]))|[^\s,]*?)(?P<version>(?:[0-9]+[\._])*[0-9]+)(?P<suffix>[^\s,]*)'
            )
        parts = separator.match(name)
        if parts:
            if parts.group('prefix'):
                self.prefix = parts.group('prefix')
            if parts.group('suffix'):
                self.suffix = parts.group('suffix')
            if parts.group('version'):
                self.number = parts.group('version')

        if not version_separator:
            version_separator = re.compile(r'([0-9]+)')
        version_parts = version_separator.findall(self.number)
        self.numbers = [int(version_part) for version_part in version_parts]
        if len(self.numbers) == 1:
            self.numbers.append(0)
        if len(self.numbers) == 2:
            self.numbers.append(0)
        #TODO handle dinamic
        self.number = '.'.join([str(v) for v in self.numbers])
