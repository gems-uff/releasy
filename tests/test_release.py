
import pytest

from releasy.release import Release

class describe_release_version:

    def it_normalizes_version_numbers(self):
        """normalizes version numbers"""
        v1 = Release(None, "1.2.3", None).version
        assert v1.normalize(1) == [1]
        assert v1.normalize(2) == [1, 2]
        assert v1.normalize(3) == [1, 2, 3]
        assert v1.normalize(4) == [1, 2, 3, 0]


    def it_calculates_diff_vector(self):
        """calculates diff"""
        v1 = Release(None, "1.0.0", None).version
        v2 = Release(None, "1.0.1", None).version
        result = v1.diff(v2)
        assert result == [0, 0, -1]

        v1 = Release(None, "2.0.0", None).version
        v2 = Release(None, "1.0.1", None).version
        result = v1.diff(v2)
        assert result == [1, 0, -1]
