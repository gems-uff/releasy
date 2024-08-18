
class Change:
    """ 
    A change in a release, such as a commit
    """
    def __init__(self, id: str) -> None:
        self._id = id
    
    @property
    def id(self) -> str:
        return self._id

    def __hash__(self) -> int:
        if self.id:
            return hash(self.id)
        else:
            return super.__hash__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Change):
            return False

        return self.id == other.id


