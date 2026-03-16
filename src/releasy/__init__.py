"""Releasy - A Release Mining Tool

Public, small surface exported here. Heavy implementation details live in
subpackages (for example `releasy.miners`).
"""

__version__ = "5.0.0-alpha.1"

from pathlib import Path

def mine(path: str | Path, configuration=None):
    """Factory that returns a mining session.

    This uses a lazy import so importing `releasy` is cheap and avoids
    pulling in implementation modules until actually used.
    """
    from .session import ReleasySession
    return ReleasySession(path, configuration)

__all__ = ["__version__", "mine"]


