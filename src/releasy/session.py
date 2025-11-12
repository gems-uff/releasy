"""Session manager for release mining operations.

This module holds the Session implementation. It lives at the package root
so it can serve as a clear entry point for developers.
"""


from typing import Any, Iterator, Optional
from pathlib import Path
from releasy.models.release import ReleaseList
from releasy.models.commit import CommitList
from releasy.configuration import Configuration

class ReleasySession:
    """Session manager for release mining operations"""

    def __init__(self, path: str | Path, config: Optional[Configuration] = None):
        # store the absolute path for predictable behavior
        self.path = Path(path).absolute()
        self._repository = None
        self.releases = ReleaseList()
        self.commits = CommitList()
        self.config = config or Configuration

    def __enter__(self) -> "ReleasySession":
        """Enter the session, initializing the repository connection.

        Real initialization (opening a git repository, network connections,
        etc.) should be done here in the future.
        """
        # TODO: initialize repository/miners here
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the session, cleaning up resources."""
        # TODO: cleanup resources (close handles, etc.)
        self._repository = None

    def __iter__(self) -> Iterator:
        """Make the session directly iterable for releases."""
        yield from self.releases

__all__ = ["ReleasySession"]
