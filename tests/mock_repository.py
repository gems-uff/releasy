from typing import Set
from releasy.repository import Commit, RepositoryProxy, Tag


class MockRepositoryProxy(RepositoryProxy):
    def fetch_tags(self) -> Set[Tag]:
        tag_refs = {
            "0.0.0-alpha1":  '0',
            "v0.9.0":        '1',
            "v1.0.0":        '3',
            "v1.0.2":        '13',
            "1.1.0":         '6',
            "v2.0.0-alpha1": '8',
            "v2.0.0-beta1":  '10',
            "v2.0.0"       : '14',
            "v2.0.1"       : '14',
            "v2.1.1"       : '20'
        }

        tags: Set[Tag] = set()
        for tag_ref, commit_ref in tag_refs.items():
            tag = Tag(None, tag_ref, self.fetch_commit(commit_ref))
            tags.add(tag)

        return tags
    
    def fetch_commit(self, id: str) -> Commit:
        commit = Commit(None, id)
        return commit

    def fetch_commit_parents(self, commit: Commit) -> Set[Commit]:
        parent_refs = {
            '1':  ['0'],
            '2':  ['1'],
            '3':  ['2'],
            '4':  ['3'],
            '5':  ['2'],
            '6':  ['5'],
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
            '20': ['19', '18'],
            '21': ['20']
        }

        parents: Set[Commit] = set()
        for commit_ref in parent_refs[commit.id]:
            parent = self.fetch_commit(commit_ref)
            parents.add(parent)
        return parents
