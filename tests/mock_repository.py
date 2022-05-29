from typing import Set
from releasy.repository import Commit, Tag


class MockRepositoryProxy():
    def __init__(self):
        self.repository = None

    def get_tags(self) -> Set[Tag]:
        tag_refs = {
            "v2.0.0": '14'
        }

        tags: Set[Tag] = set()
        for tag_ref, commit_ref in tag_refs.items():
            tag = Tag(self.repository, tag_ref, self.get_commit(commit_ref))

        tags = self.proxy.get_tags()
        return tags
    
    def get_commit(self, id: str) -> Commit:
        commit = Commit(self.repository, id)
        return commit

    def get_parents(self, commit: Commit) -> Set[Commit]:
        parent_refs = {
            '1': ['0'],
            '2': ['1'],
            '3': ['2'],
            '4': ['3'],
            '5': ['2'],
            '6': ['5'],
            '7': ['4', '6'],
            '8': ['7'],
            '9': ['8'],
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
            '20': ['19', '18'],
            '21': ['20']
        }

        parents: Set[Commit] = set()
        for commit_ref in parent_refs[commit.id]:
            parents.add(self.get_commit(commit_ref))
        return parents
