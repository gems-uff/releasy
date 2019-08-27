from releasy.model import Commit, Developer, Tag
from releasy.miner import Vcs


class VcsMock(Vcs):
    def __init__(self):
        # id, parents, tag
        a1 = Developer()
        commit_data = [
            (0 ,[]   ,a1,a1,[]),
            (1 ,[0]  ,a1,a1,["v1.0.0"]),
            (2 ,[1]  ,a1,a1,["v1.0.1"]),
            (3 ,[2]  ,a1,a1,[]),
            (4 ,[1]  ,a1,a1,[]),
            (5 ,[4]  ,a1,a1,["v1.1.0"]),
            (6 ,[3,5],a1,a1,[]),
            (7 ,[6]  ,a1,a1,["v2.0.0-apha1"]),
            (8 ,[7]  ,a1,a1,[]),
            (9 ,[8]  ,a1,a1,["v2.0.0-beta1"]),
            (10,[9]  ,a1,a1,["v2.0.0"]),
            (11,[10] ,a1,a1,[]),
        ]
        
        commits = {}
        tags = []
        for (index, parents_index, author, committer, tagnames) in commit_data:
            parents = [commits[p_index] for p_index in parents_index]
            commits[index] = Commit(id=index,
                                    parents=parents,
                                    author=author, 
                                    committer=committer,
                                    message="Commit %d" % index)
            for tagname in tagnames:
                tags.append(Tag(tagname, commits[index]))

        self._commits = commits
        self._tags = tags

    def tags(self):
        return self._tags
    
    def commits(self):
        return self._commits
