"""Test the main ReleasySession functionality (pyspec style)"""

from pathlib import Path
import releasy as rle
from releasy.session import ReleasySession
from releasy.models.release import ReleaseList
from releasy.models.commit import CommitList

class DescribeReleasySession():
    def it_has_a_list_of_the_Releases(self):
        with rle.mine(".") as session:
            assert hasattr(session, "releases")
            assert isinstance(session.releases, ReleaseList)

    def it_has_a_list_of_the_Commits_of_the_Releases(self):
        with rle.mine(".") as session:
            assert hasattr(session, "commits")
            assert isinstance(session.commits, CommitList)
