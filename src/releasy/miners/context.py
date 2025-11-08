"""Context manager for release mining operations.

This module holds the ReleasyContext implementation. It lives under
`releasy.miners` so the package top-level can stay lightweight and only
re-export small public symbols.
"""

from typing import Any, Iterator
from pathlib import Path


class ReleasyContext:
    """Context manager for release mining operations"""

    def __init__(self, path: str | Path):
        # store the absolute path for predictable behavior
        self.path = Path(path).absolute()
        self._repository = None

    def __enter__(self) -> "ReleasyContext":
        """Enter the context, initializing the repository connection.

        Real initialization (opening a git repository, network connections,
        etc.) should be done here in the future.
        """
        # TODO: initialize repository/miners here
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context, cleaning up resources."""
        # TODO: cleanup resources (close handles, etc.)
        self._repository = None

    def __iter__(self) -> Iterator:
        """Make the context directly iterable for releases."""
        # TODO: yield actual release objects once mining is implemented
        yield from []


__all__ = ["ReleasyContext"]
