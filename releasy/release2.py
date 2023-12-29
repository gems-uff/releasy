from typing import Self, Set
from abc import ABC

from datetime import datetime, timedelta

from .change import Change


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
    def __init__(self) -> None:
        self.release: Release = Release()
    
    def name(self, name: str) -> Self:
        self.release.name = name
        return self
        
    def build(self) -> Release:
        release = self.release
        self.release = Release()
        return release
