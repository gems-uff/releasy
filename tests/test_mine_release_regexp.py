# from datetime import datetime, timedelta
# import pytest

# from releasy.miner_legacy import Miner
# from releasy.exception import MisplacedTimeException

# from .mock import DifferentReleaseNameVcsMock


# def test_mine_release_prefixes():
#     miner = Miner(vcs=DifferentReleaseNameVcsMock(), release_prefixes=["v",""])
#     project = miner.mine_releases()
#     assert len(project.releases) == 8
#     assert project.releases[0].version == "0.0.0"
#     assert project.releases[1].version == "0.1.0"
#     assert project.releases[2].version == "1.0.0"
#     assert project.releases[3].version == "1.0.0"
#     assert project.releases[4].version == "1.0.0"
#     assert project.releases[5].version == "1.0.0"
#     assert project.releases[6].version == "1.0.0"
#     assert project.releases[7].version == "3.0.0"
#     assert len(project.release_prefixes) == 2
#     assert "v" in project.release_prefixes
#     assert "" in project.release_prefixes


# def test_mine_release_suffixes(): #TODO: ignored suffix should affect only pre_releases
#     miner = Miner(vcs=DifferentReleaseNameVcsMock(), release_prefixes=["v",""], ignored_suffixes=["Final"])
#     project = miner.mine_releases()
#     assert not project.releases[0].suffix
#     assert not project.releases[1].suffix
#     assert not project.releases[2].suffix
#     assert project.releases[3].suffix == "beta1"
#     assert project.releases[4].suffix == "beta2"
#     assert project.releases[5].suffix == "a1"
#     assert project.releases[6].suffix == "b1"
#     assert not project.releases[7].suffix
#     assert len(project.release_suffixes) == 5
#     assert "" in project.release_suffixes
#     assert "a1" in project.release_suffixes
#     assert "b1" in project.release_suffixes
#     assert "beta1" in project.release_suffixes
#     assert "beta2" in project.release_suffixes
#     assert "Final" not in project.release_suffixes


# def test_mine_release_version_separator():
#     miner = Miner(vcs=DifferentReleaseNameVcsMock(), version_separator="_")
#     project = miner.mine_releases()
#     assert len(project.releases) == 1
#     assert project.releases[0].version == "2.0.1"
