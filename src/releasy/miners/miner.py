from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from releasy.configuration import Configuration
from releasy.models.project import Project


class MinerPlugin(ABC):
    def __init__(self, config: Optional[Configuration] = None) -> None:
        self.config = config

    def set_configuration(self, config: Configuration) -> None:
        self.config = config

    @abstractmethod
    def mine(self, project: Project) -> Project:
        pass


class Miner:
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def mine(self) -> Project:
        project = Project()
        for plugin in self.config.plugins:
            if hasattr(plugin, "set_configuration"):
                plugin.set_configuration(self.config)
            project = plugin.mine(project)
        return project
