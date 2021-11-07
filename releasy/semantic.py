
from .release import (Release)

class MainRelease:
    def __init__(self, release: Release) -> None:
        self.release = release
        self.pre_releases = []
        self.patches = []


class PreRelease:
    pass


class Patch:
    pass

