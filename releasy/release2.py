from typing import Self, Set, Tuple
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


class ReleaseVersion:
    pass


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


class ReleaseFactory(ABC):
    @abstractmethod
    def create(self, name, version) -> Release:
        pass 
    

class MainReleaseFactory(ReleaseFactory):
    def create(self, name, version):
        return MainRelease(name, version)
    

class ReleaseVersioningSchema(ABC):
    @abstractmethod
    def parse(self, name: str) -> Tuple[ReleaseVersion, ReleaseFactory]:
        pass


class SimpleVersioningSchema(ReleaseVersioningSchema):
    def parse(self, name: str) -> Tuple[str, ReleaseVersion]:
        return SimpleReleaseVersion(name), MainReleaseFactory()


class SemanticReleaseFactory(ReleaseFactory):
    def create(self, name: str, version: SemanticVersion) -> Release:
        if version.patch:
            return Patch(name, version)
        if version.minor:
            return MinorRelease(name, version)
        if version.major:
            return MajorRelease(name, version)
        return None
       

class SemanticVersioningSchema(ReleaseVersioningSchema):
    def parse(self, name: str) -> Tuple[str, ReleaseVersion]:
       version = SemanticVersion(name)
       return version, SemanticReleaseFactory()


class ReleaseBuilder:
    def __init__(self, 
                 versioning_schema: ReleaseVersioningSchema = None) -> None:
        if versioning_schema:
            self._version_schema = versioning_schema
        else:
            self._version_schema = SimpleVersioningSchema()
        self.reset()
    
    def reset(self):
        self._name = ""
        
    def name(self, name: str) -> Self:
        self._name = name
        return self
        
    def build(self) -> Release:
        version, factory = self._version_schema.parse(self._name)
        release = factory.create(self._name, version)
        return release


