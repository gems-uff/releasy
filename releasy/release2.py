from typing import Self, Set
from abc import ABC, abstractmethod

from datetime import datetime, timedelta

from releasy.version import ReleaseVersioningSchema, SimpleVersioningSchema
from releasy.change import Change


class Release(ABC):
    def __init__(self) -> None:
        self.name: str = None
        self.version: ReleaseVersion = None
        self.changes: Set[Change] = ()
        self.lifecycle: ReleaseLifeCycle = None
        self.cycle: timedelta = None
        self.base_releases: Set[Release] = ()


class FinalRelease(Release):
    pass


class MainRelease(FinalRelease):
    pass


class MajorRelease(MainRelease):
    pass


class MinorRelease(MainRelease):
    pass


class Patch(FinalRelease):
    pass


class PreRelease(Release):
    pass


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
        self.name = name
        return self
        
    def build(self) -> Release:
        version, factory = self._version_schema.parse(self._name)
        release = factory.create(self.name, version)
        return release


class ReleaseFactory():
    def create(self, name, version) -> Release:
        match version:
            case "Major":
                return MajorRelease(name, version)
            case _:
                return MainRelease(name, version)
