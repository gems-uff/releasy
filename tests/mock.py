from typing import List
import pytest

from datetime import datetime, timedelta

from releasy.release import Developer
from releasy.commit import (
    Commit, 
    Tag)
from releasy.miner.source import Vcs


def vcs_data():
    dev = DevMock()
    alice = dev.alice
    bob = dev.bob
    charlie = dev.charlie
    one_day = timedelta(days=1)
    one_hour = timedelta(hours=1)
    return [  
        (0 ,[]     ,alice  ,alice  ,one_day,None    ,[]),
        (1 ,[0]    ,alice  ,bob    ,one_day,one_hour,["v1.0.0"]),          #r0
        (2 ,[1]    ,bob    ,bob    ,one_day,None    ,[]),
        (3 ,[2]    ,bob    ,bob    ,one_day,one_hour,["v1.0.1"]),          #r1
        (4 ,[3]    ,alice  ,alice  ,one_day,None    ,["non-release"]),
        (5 ,[2]    ,alice  ,alice  ,one_day,None    ,[]),
        (6 ,[5]    ,alice  ,alice  ,one_day,None    ,["v1.1.0"]),          #r2
        (7 ,[4,6]  ,charlie,bob    ,one_day,None    ,[]),
        (8 ,[7]    ,charlie,charlie,one_day,None    ,["v2.0.0-alpha1"]),   #r3
        (9 ,[8]    ,alice  ,bob    ,one_day,None    ,[]),
        (10,[9]    ,alice  ,alice  ,one_day,None    ,["v2.0.0-beta1"]),    #r4
        (11,[2]    ,alice  ,alice  ,one_day,None    ,[]),
        (12,[10,11],alice  ,alice  ,one_day,None    ,[]),
        (13,[3]    ,alice  ,alice  ,one_day,None    ,["v1.0.2"]),
        (14,[13,12],alice  ,alice  ,one_day,one_hour,["v2.0.0", "v2.0.1"]),#r5,6
        (15,[14]   ,alice  ,alice  ,one_day,None    ,[]),
        (16,[15]   ,alice  ,alice  ,one_day,None    ,[]),
        (17,[14]   ,alice  ,alice  ,one_day,None    ,[]),
        (18,[16,10],alice  ,alice  ,one_day,None    ,[]),
        (19,[16,17],alice  ,alice  ,one_day,None    ,[]),
        (20,[18,19],alice  ,alice  ,one_day,None    ,["v2.1.0"]),         #r7
        (21,[20]   ,alice  ,alice  ,one_day,None    ,[]),
    ]


# def c():
#     commit_data = [  
#         (0 ,[]),
#         (1 ,[0]),
#         (2 ,[1]),
#         (3 ,[2]),
#         (4 ,[3]),
#         (5 ,[2]),
#         (6 ,[5]),
#         (7 ,[4,6]),
#         (8 ,[7]),
#         (9 ,[8]),
#         (10,[9]),
#         (11,[2]),
#         (12,[10,11]),
#         (13,[3]),
#         (14,[13,12]),
#         (15,[14]),
#         (16,[15]),
#         (17,[14]),
#         (18,[16,10]),
#         (19,[16,17]),
#         (20,[18,19]),
#         (21,[20])
#     ]
#     for commit in commit_data:


def retrieve_commits(vcs_data) -> List[Commit]:
    ref_dt = datetime(2020, 1, 1, 12, 00)        
    commit_data = vcs_data
    commits = [] 
    for (index, parents_index, author, committer, increment_dt, offset, tagnames) in commit_data:
        parents = [commits[p_index] for p_index in parents_index]
        commits.append(Commit(hashcode = index,
                              parents = parents,
                              author = author,
                              author_time = ref_dt,
                              committer = committer,
                              committer_time = ref_dt,
                              message = "Commit %d" % index))
        ref_dt += increment_dt
    return commits


def assign_tags_to_commits(commits):
    tag_to_commit_map = {
        'v1.0.0': 1,
        'v1.0.1': 3,
        'non-release': 4,
        '1.1.0': 6,
        'v2.0.0-alpha1': 8,
        'v2.0.0-beta1': 10,
        'v1.0.2': 13,
        'v2.0.0': 14,
        'v2.0.1': 14,
        'v2.1.0': 14
    }
    for tag_name, commit_index in tag_to_commit_map.items():
        tag = Tag(
            name=tag_name,
            commit=commits[commit_index])


def assign_releases_to_tags():
    tags = []
    for tag in tags:
        if tag.name != 'non-release':
            pass


@pytest.fixture
def commits():
    mock = VcsMock()
    return mock.commits()


class VcsMock(Vcs):
    def __init__(self, path="./releasy"):
        super().__init__(path)
        # Start Date and incremetns
        ref_dt = datetime(2020, 1, 1, 12, 00)        
        one_day = timedelta(days=1)
        one_hour = timedelta(hours=1)
        
        # Developers
        self.dev = DevMock()
        alice = self.dev.alice
        bob = self.dev.bob
        charlie = self.dev.charlie

        # Commits
        # id, parents, author, committer, time increment, tag, tag time increment
        commit_data = [  
            (0 ,[]     ,alice  ,alice  ,one_day,None    ,[]),
            (1 ,[0]    ,alice  ,bob    ,one_day,one_hour,["v1.0.0"]),          #r0
            (2 ,[1]    ,bob    ,bob    ,one_day,None    ,[]),
            (3 ,[2]    ,bob    ,bob    ,one_day,one_hour,["v1.0.1"]),          #r1
            (4 ,[3]    ,alice  ,alice  ,one_day,None    ,["non-release"]),
            (5 ,[2]    ,alice  ,alice  ,one_day,None    ,[]),
            (6 ,[5]    ,alice  ,alice  ,one_day,None    ,["1.1.0"]),          #r2
            (7 ,[4,6]  ,charlie,bob    ,one_day,None    ,[]),
            (8 ,[7]    ,charlie,charlie,one_day,None    ,["v2.0.0-alpha1"]),   #r3
            (9 ,[8]    ,alice  ,bob    ,one_day,None    ,[]),
            (10,[9]    ,alice  ,alice  ,one_day,None    ,["v2.0.0-beta1"]),    #r4
            (11,[2]    ,alice  ,alice  ,one_day,None    ,[]),
            (12,[10,11],alice  ,alice  ,one_day,None    ,[]),
            (13,[3]    ,alice  ,alice  ,one_day,None    ,["v1.0.2"]),
            (14,[13,12],alice  ,alice  ,one_day,one_hour,["v2.0.0", "v2.0.1"]),#r5,6
            (15,[14]   ,alice  ,alice  ,one_day,None    ,[]),
            (16,[15]   ,alice  ,alice  ,one_day,None    ,[]),
            (17,[14]   ,alice  ,alice  ,one_day,None    ,[]),
            (18,[16,10],alice  ,alice  ,one_day,None    ,[]),
            (19,[16,17],alice  ,alice  ,one_day,None    ,[]),
            (20,[18,19],alice  ,alice  ,one_day,None    ,["v2.1.0"]),         #r7
            (21,[20]   ,alice  ,alice  ,one_day,None    ,[]),
        ]

        commits = {}
        tags = []
        for (index, parents_index, author, committer, increment_dt, offset, tagnames) in commit_data:
            parents = [commits[p_index] for p_index in parents_index]
            commits[index] = Commit(hashcode = index,
                                    parents = parents,
                                    author = author,
                                    author_time = ref_dt,
                                    committer = committer,
                                    committer_time = ref_dt,
                                    message = "Commit %d" % index)
            tag_offset = ref_dt
            for tagname in tagnames:
                if offset:
                    tag_offset += offset
                    tag = Tag(name=tagname, 
                              commit=commits[index], 
                              time=tag_offset, 
                              message=f"tag {tagname}")
                else:
                    tag = Tag(name=tagname, 
                              commit=commits[index])
                tags.append(tag)
            
            ref_dt += increment_dt

        self._commits = commits
        self._tags = tags

    def tags(self):
        return self._tags
    
    def commits(self):
        return list(self._commits.values())

class DifferentReleaseNameVcsMock(Vcs):
    def __init__(self):
        super().__init__("./releasy")

        ref_dt = datetime(2020, 1, 1, 12, 00)        
        one_day = timedelta(days=1)
        dev = DevMock()
        alice = dev.alice

        commit_data = [  
            "v0.0.0",
            "v0.1",
            "1.0.0",
            "v1.0.0-beta1",
            "v1.0.0beta2",
            "v1.0.0a1",
            "v1.0.0.b1",
            "n2.0.0",
            "v2_0_1",
            "3.0.0Final"
        ]

        commits = {}
        tags = []
        parents = []
        index = 1
        for tagname in commit_data:
                commits[index] = Commit(hashcode=index,
                                        parents=parents,
                                        author=alice, 
                                        author_time=ref_dt,
                                        committer=alice,
                                        committer_time=ref_dt,
                                        message="Commit %d" % index)
                tag = Tag(name=tagname, 
                          commit=commits[index], 
                          time=ref_dt, 
                          message=f"tag {tagname}")
                tags.append(tag)

                parents = [index]
                index += 1
                ref_dt += one_day

        self._commits = commits
        self._tags = tags


class MisplacedTimeVcsMock(Vcs):
    def __init__(self, misplaced_commits, path="./releasy"):
        super().__init__(path)
        ref_dt = datetime(2020, 1, 1, 12, 00)
        misplaced_dt = datetime(1990, 1, 1, 00, 00)
        one_day = timedelta(days=1)
        self.dev = DevMock()
        alice = self.dev.alice
        
        self._tags = []
        commits = []

        parents = []
        for index in range(12):
            commit_ref_dt = ref_dt
            if index in misplaced_commits:
                commit_ref_dt = misplaced_dt

            commit = Commit(hashcode=index,
                            parents=parents,
                            author=alice, 
                            author_time=commit_ref_dt,
                            committer=alice,
                            committer_time=commit_ref_dt,
                            message="Commit %d" % index)
            commits.append(commit)

            if ((index+1) % 4 == 0):
                tag = Tag(name=f"1.1.{int(index/4)}", 
                          commit=commit)
                self._tags.append(tag) 

            ref_dt += one_day                            
            parents = [commit]


    def tags(self):
        return self._tags
    

class DevMock():
    def __init__(self):
        self.alice = Developer(login="alice", name="Mrs. Alice", email="alice@example.com")
        self.bob = Developer(login="bob", name="Mrs. Bob", email="bob@example.com")
        self.charlie = Developer(login="charlie", name="Mr. Charlie", email="charlie@example.com")
