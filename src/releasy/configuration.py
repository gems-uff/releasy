"""Configuration object for Releasy mining sessions.

This class holds options for customizing the mining process. Options can be
added as needed during development.
"""
from __future__ import annotations

from typing import Optional, List

from releasy.version_format import ReleaseVersionFormat, SemanticVersioningFormat

class Configuration:
    def __init__(
        self,
        branch: Optional[str] = None,
        plugins: Optional[List] = None,
        release_miners: Optional[List[str]] = None,
        release_prefixes: Optional[List[str]] = None,
        ignore_tags: Optional[List[str]] = None,
        version_format: Optional[ReleaseVersionFormat] = None,
        commit_strategy=None,
        log_level: Optional[str] = None,
    ):
        self.branch = branch
        self.plugins = plugins or []
        self.release_miners = release_miners or []
        self.release_prefixes = release_prefixes or []
        self.ignore_tags = ignore_tags or []
        self.version_format = version_format or SemanticVersioningFormat()
        if commit_strategy is None:
            from releasy.miners.strategy import HistoryBasedStrategy

            commit_strategy = HistoryBasedStrategy()
        self.commit_strategy = commit_strategy
        self.log_level = log_level

    @property
    def parser(self) -> ReleaseVersionFormat:
        """Compatibility alias used by legacy miners."""
        return self.version_format

    def __repr__(self):
        return (
            f"<Configuration branch={self.branch!r} "
            f"plugins={self.plugins!r} "
            f"release_miners={self.release_miners!r} "
            f"release_prefixes={self.release_prefixes!r} "
            f"ignore_tags={self.ignore_tags!r} "
            f"version_format={self.version_format!r} "
            f"commit_strategy={self.commit_strategy!r} "
            f"log_level={self.log_level!r}>"
        )

    @staticmethod
    def default() -> "Configuration":
        """Create a Configuration object with default settings."""
        return Configuration(version_format=SemanticVersioningFormat())
