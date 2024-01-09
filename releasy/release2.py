from typing import List, Self, Set, Tuple
from abc import ABC, abstractmethod

from datetime import datetime, timedelta

from releasy.version import (
    ReleaseVersion,
    SemanticVersion, 
    SimpleReleaseVersion 
)
from releasy.change import Change


class Release(ABC):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        self.name = name
        self.version = version
        self.description = ''
        self.developer: str = None
        self.timestamp: datetime = None
        self.changes: Set[Change] = ()
        self.lifecycle: ReleaseLifeCycle = None
        self.cycle: timedelta = None
        self.base_releases: Set[Release] = ()


class FinalRelease(Release):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        super().__init__(name, version)


class MainRelease(FinalRelease):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        super().__init__(name, version)


class MajorRelease(MainRelease):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        super().__init__(name, version)


class MinorRelease(MainRelease):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        super().__init__(name, version)


class Patch(FinalRelease):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        super().__init__(name, version)


class PreRelease(Release):
    def __init__(self, name: str, version: ReleaseVersion) -> None:
        super().__init__(name, version)


class ReleaseLifeCycle:
    def __init__(self) -> None:
        self.development: ReleaseDevelopmentLifeCycle = None
        self.delivery: ReleaseDeliveryLifeCycle = None


class ReleaseDevelopmentLifeCycle:
    def __init__(self) -> None:
        self.start: datetime = None
        self.end: datetime = None
        self.start_delay: timedelta = None
        self.duration: timedelta = None
        

class ReleaseStabilizationLifeCycle:
    def __init__(self) -> None:
        self.start: datetime = None
        self.end: datetime = None
        self.duration: timedelta = None
        

class ReleaseDeliveryLifeCycle:
    def __init__(self) -> None:
        self.time: datetime = None
        self.delay: timedelta = None


class ReleaseVersioningSchema(ABC):
    @abstractmethod
    def apply(self, name: str) -> Release:
        """ Create a release from its reference name """
        pass


class SimpleVersioningSchema(ReleaseVersioningSchema):
    def apply(self, name: str) -> Release:
        try:
            version = SimpleReleaseVersion(name)
            return MainRelease(name, version)
        except:
            pass
        return None


class SemanticVersioningSchema(ReleaseVersioningSchema):
    def apply(self, name: str) -> Release:
        try:
            version = SemanticVersion(name)
            if version.patch:
                return Patch(name, version)
            if version.minor:
                return MinorRelease(name, version)
            if version.major:
                return MajorRelease(name, version)
        except:
            pass
        return None
       

class ReleaseReference:
    def __init__(self, name: str, timestamp: datetime, developer: str,
                 description: str, change_refs: List[str]) -> None:
        self.name = name
        self.timestamp = timestamp
        self.developer = developer
        self.description = description
        self.change_refs = change_refs


class ReleaseBuilder:
    def __init__(self, versioning_schema: ReleaseVersioningSchema = None) -> None:
        self._version_schema = versioning_schema or SimpleVersioningSchema()
        self.reset()
    
    def reset(self):
        self._reference = None 

    def reference(self, reference: ReleaseReference) -> Self:
        self._reference = reference 
        return self

    def build(self) -> Release:
        release = self._version_schema.apply(self._reference.name)
        if not release:
            return None
        release.description = self._reference.description
        release.timestamp = self._reference.timestamp
        release.developer = self._reference.developer
        return release
