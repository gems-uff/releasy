from datetime import datetime, timedelta, timezone
from typing import List, Set

import pygit2

from releasy.miner.base import ReleaseMiner
from releasy.miner.repository import Repository
from releasy.release2 import Release, ReleaseReference


class GitRepository(Repository):
    """ A Git Repository Abstraction """
    def __init__(self, path) -> None:
        super().__init__()
        self._path = path
        self._git = pygit2.Repository(path)

    @property
    def release_refs(self) -> List[ReleaseReference]:
        tags: List[pygit2.Reference] = [
            tag for tag in self._git.references.objects 
            if tag.name.startswith('refs/tags/')
        ]

        targets = [
            self._git.get(tag_reference.target) 
            for tag_reference in tags
        ]

        references = map(
            lambda tag, target: create_reference(tag, target),
            tags, targets
        )
        references = [ref for ref in references if ref]
        return references


def create_reference(
            tag_ref: pygit2.Reference, 
            target_ref: pygit2.Object
        ) -> ReleaseReference: 
    
    match target_ref:
        case pygit2.Tag() as tag:
           timestamp = get_time(tag.tagger)
           developer = f'{tag.tagger.name} <{tag.tagger.email}>'
           description = tag.message
           commit = tag.peel(pygit2.Commit)
           change_refs = [commit.oid] if commit else []
        case pygit2.Commit() as commit:
           timestamp = get_time(commit.committer)
           developer = f'{commit.committer.name} <{commit.committer.email}>'
           description = commit.message
           change_refs = [commit.oid]
        case _:
           return None 
    return ReleaseReference(tag_ref.shorthand, timestamp, developer, description,
                            change_refs)


def get_time(tagger):
    time_tzinfo = timezone(timedelta(minutes=tagger.offset))
    time = datetime.fromtimestamp(float(tagger.time), time_tzinfo)
    return time
