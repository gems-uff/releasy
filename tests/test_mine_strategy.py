import releasy
import releasy.mine_strategy

def test():
    str = releasy.mine_strategy.TimeMineStrategy("a")
    assert str.vcs == "a"
    assert 1 == 1