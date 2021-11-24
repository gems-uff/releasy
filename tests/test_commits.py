

from typing import List
from releasy.commit import (
    Commit
)

from .mock import commits

def describe_commit():
    def it_has_id(commits: List[Commit]):
        for index, commit in enumerate(commits):
            assert commit.id == index

    def it_has_full_history(commits: List[Commit]):
        assert not commits[0].history()
        assert commits[1].history() == set([commits[0]])
        assert commits[3].history() == commits[2].history(include_self=True)
        assert commits[6].history() == commits[5].history(include_self=True)
        assert commits[7].history() \
            == commits[4].history(include_self=True) \
             | commits[6].history(include_self=True)
        assert commits[12].history() \
            == commits[10].history(include_self=True) \
             | commits[11].history(include_self=True)
        
    def it_has_partial_history(commits: List[Commit]):
        assert commits[3].history(unreachable_by=set([commits[1]])) \
            == set([commits[2]])
        assert commits[14].history(
            unreachable_by=set([commits[3], commits[6], commits[13]])) \
            == set([commits[12], commits[11], commits[10], commits[9],
                    commits[8], commits[7], commits[4]])
        assert not commits[12].history(unreachable_by=[commits[14]])
