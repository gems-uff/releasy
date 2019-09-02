from datetime import datetime, timedelta

from releasy.model import Commit, Developer, Tag
from releasy.miner import Vcs


class VcsMock(Vcs):
    def __init__(self, path):
        super().__init__(path)
        # Start Date and incremetns
        ref_dt = datetime(2020, 1, 1, 12, 00)        
        one_day = timedelta(days=1)
        
        # Developers
        alice = Developer()
        bob = Developer()
        charlie = Developer()

        # Commits
        # id, parents, author, committer, time increment, tag, tag time increment
        commit_data = [  
            (0 ,[]     ,alice  ,alice  ,one_day,[]),
            (1 ,[0]    ,alice  ,alice  ,one_day,["v1.0.0"]),          #r0
            (2 ,[1]    ,bob    ,bob    ,one_day,[]),
            (3 ,[2]    ,bob    ,bob    ,one_day,["v1.0.1"]),          #r1
            (4 ,[3]    ,alice  ,alice  ,one_day,[]),
            (5 ,[2]    ,alice  ,alice  ,one_day,[]),
            (6 ,[5]    ,alice  ,alice  ,one_day,["v1.1.0"]),          #r2
            (7 ,[4,6]  ,bob    ,bob    ,one_day,[]),
            (8 ,[7]    ,charlie,charlie,one_day,["v2.0.0-alpha1"]),   #r3
            (9 ,[8]    ,alice  ,bob    ,one_day,[]),
            (10,[9]    ,alice  ,alice  ,one_day,["v2.0.0-beta1"]),    #r4
            (11,[2]    ,alice  ,alice  ,one_day,[]),
            (12,[10,11],charlie,charlie,one_day,[]),
            (13,[12]   ,alice  ,alice  ,one_day,["v2.0.0", "v2.0.1"]),#r5,6
            (14,[13]   ,alice  ,alice  ,one_day,[]),
        ]

        commits = {}
        tags = []
        for (index, parents_index, author, committer, increment_dt, tagnames) in commit_data:
            parents = [commits[p_index] for p_index in parents_index]
            commits[index] = Commit(hashcode=index,
                                    parents=parents,
                                    author=author, 
                                    author_time=ref_dt,
                                    committer=committer,
                                    committer_time=ref_dt,
                                    message="Commit %d" % index)
            for tagname in tagnames:
                tags.append(Tag(tagname, commits[index]))
            
            ref_dt += increment_dt

        self._commits = commits
        self._tags = tags

    def tags(self):
        return self._tags
    
    def commits(self):
        return self._commits
