from typing import Set
from datetime import datetime, timedelta
from releasy.repository import Commit, CommitSet, Repository, RepositoryProxy, Tag


class MockRepositoryProxy(RepositoryProxy):
    def __init__(self, ref_dt: datetime) -> None:
        super().__init__()
        self.ref_dt = ref_dt
        self.name = 'mock'

    def fetch_tags(self) -> Set[Tag]:
        tag_refs = {
            "0.0.0-alpha1":  '0',
            "v0.9.0":        '1',
            "0.10.1":        '5',
            "v1.0.0":        '3',
            "r-1.0.2":       '13',
            "1.1.0":         '6',
            "1.1.1":         '7',
            "v2.0.0-alpha1": '8',
            "v2.0.0-beta1":  '10',
            "v2.0.0":        '14',
            "2.0":           '15',
            "v2.0.1":        '14',
            "rel2.1.1pre":   '17',
            "v2.1":          '20',
            "non":           '18',
            "v3.1.0":        '22',
            "v3.1.1":        '19',
            "v4.0.0":        '21'
        }

        tags: Set[Tag] = set()
        for tag_ref, commit_ref in tag_refs.items():
            tag = Tag(self.repository, tag_ref, self.repository.get_commit(commit_ref))
            tags.add(tag)

        return tags
    
    def fetch_commit(self, id: str) -> Commit:
        pos = int(id)

        committers = {
            '2': 'bob',
            '3': 'bob',
            '7': 'charlie',
            '8': 'charlie'
        }
        if id in committers:
            committer = committers[id]
        else: 
            committer = 'alice'
        committer_date = self.ref_dt + timedelta(days=1) * pos

        authors = {
            '1':  'bob',
            '2':  'bob',
            '3':  'bob',
            '7':  'bob',
            '8':  'charlie',
            '9':  'bob',
            '12': 'bob'
        }
        if id in authors:
            author = authors[id]
        else: 
            author = 'alice'
        author_date = committer_date

        commit = Commit(
            self.repository,
            id,
            id,
            committer,
            committer_date,
            author,
            author_date)

        return commit

    def fetch_commit_parents(self, commit: Commit) -> CommitSet:
        parent_refs = {
            '1':  ['0'],
            '2':  ['1'],
            '3':  ['2'],
            '4':  ['3'],
            '6':  ['5', '2'],
            '7':  ['4' , '6'],
            '8':  ['7'],
            '9':  ['8'],
            '10': ['9'],
            '11': ['2'],
            '12': ['10', '11'],
            '13': ['3'],
            '14': ['12', '13'],
            '15': ['14'],
            '16': ['15'],
            '17': ['14'],
            '18': ['10', '16'],
            '19': ['17'],
            '20': ['18'],
            '21': ['19', '18'],
            '22': ['20'],
            '23': ['21'],
        }

        parents = CommitSet()
        if commit.id in parent_refs:
            for commit_ref in parent_refs[commit.id]:
                parent = self.repository.get_commit(commit_ref)
                parents.add(parent)
        return parents

    def diff(self, commit_a: Commit, commit_b: Commit):
        pass


class MockRepository(Repository):
    ref_dt = datetime(2020, 1, 1, 12, 00)    
    
    def __init__(self):
        super().__init__(MockRepositoryProxy(MockRepository.ref_dt))
