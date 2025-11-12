"""Configuration object for Releasy mining sessions.

This class holds options for customizing the mining process. Options can be
added as needed during development.
"""
from typing import Optional, List

class Configuration:
    def __init__(
        self,
        branch: Optional[str] = None,
        release_miners: Optional[List[str]] = None,
        release_prefixes: Optional[List[str]] = None,
        ignore_tags: Optional[List[str]] = None,
        log_level: Optional[str] = None,
    ):
        self.branch = branch
        self.release_miners = release_miners or []
        self.release_prefixes = release_prefixes or []
        self.ignore_tags = ignore_tags or []
        self.log_level = log_level

    def __repr__(self):
        return (
            f"<Configuration branch={self.branch!r} "
            f"release_miners={self.release_miners!r} "
            f"release_prefixes={self.release_prefixes!r} "
            f"ignore_tags={self.ignore_tags!r} "
            f"log_level={self.log_level!r}>"
        )

    @staticmethod
    def default() -> "Configuration":
        """Create a Configuration object with default settings."""
        return Configuration()
