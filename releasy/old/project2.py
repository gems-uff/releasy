
from typing import Set

from .release2 import Release


class Project:
    def __init__(self) -> None:
        self.releases: Set[Release] = None
