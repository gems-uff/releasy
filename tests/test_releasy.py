"""Test the main Releasy functionality"""

from pathlib import Path
import releasy as rle
from releasy import __version__


def test_version():
    """Test that version is properly set"""
    assert __version__ == "5.0.0-alpha.1"


def test_context_manager():
    """Test that the context manager works properly"""
    from releasy.miners.context import ReleasyContext
    with rle.mine(".") as releases:
        assert isinstance(releases, ReleasyContext)


def test_context_manager_path():
    """Test that path is properly set"""
    test_path = Path(".")
    with rle.mine(test_path) as releases:
        assert releases.path == test_path.absolute()


def test_context_manager_iteration():
    """Test that we can iterate over releases"""
    with rle.mine(".") as releases:
        releases_list = list(releases)
        # Initially empty until we implement release mining
        assert isinstance(releases_list, list)
        assert len(releases_list) == 0


def test_str_path():
    """Test that string paths work"""
    with rle.mine("./some/path") as releases:
        assert isinstance(releases.path, Path)


def test_path_path():
    """Test that Path objects work"""
    path = Path("./some/path")
    with rle.mine(path) as releases:
        assert releases.path == path.absolute()