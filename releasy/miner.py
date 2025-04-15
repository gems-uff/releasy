
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import pygit2

from releasy.contributor import Contributor
from releasy.graph import ReleaseGraph
from releasy.old.version_format import ReleaseVersionFormat, SemanticVersioningFormat
from releasy.release import Release


@dataclass
class Configuration:
    plugins: List[str]
    parser: ReleaseVersionFormat = SemanticVersioningFormat()


class Miner:
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def mine(self):
        graph = ReleaseGraph()
        config = self.config
        for plugin in self.config.plugins:
            graph = plugin.mine(graph, config)
        return graph


class MinerPlugin(ABC):
    @abstractmethod
    def mine(self, graph: ReleaseGraph, config: Configuration):
        pass
    

class DictMiner(MinerPlugin):
    def __init__(self, dict: Dict):
        self.dict = dict

    def mine(self, graph: ReleaseGraph, config: Configuration):
        parser = config.parser
        for data in self.dict:
            version = parser.parse(data['name'])
            contributor = Contributor(data['name'])
            release = Release(
                version=version,
                timestamp=data['timestamp'],
                head=data['head'],
                author=contributor
            )
            graph.add(release)
        return graph


class GitMiner(MinerPlugin):
    def __init__(self, path: str, mine_commits: bool = True):
        self.path = path
        self.git = pygit2.Repository(self.path) 
        self.mine_commits = mine_commits

    def mine(self, graph: ReleaseGraph, config: Configuration):
        self.fetch_tags(graph, config)
        return graph
    
    def fetch_tags(self, graph: ReleaseGraph, config: Configuration) -> None:
        tag_refs = [
            ref 
            for ref in self.git.references.objects 
            if ref.name.startswith('refs/tags/')
        ]
        version_parser = config.parser

        for tag_ref in tag_refs:
            tag = self.git.get(tag_ref.target)

            version = version_parser.parse(tag_ref.shorthand)
            if not version:
                continue

            # Simple Tag
            if tag.type == pygit2.GIT_OBJECT_COMMIT:
                head = self.git.get(tag.id) #TODO Convert to commit
                author = None
                tagger_tzinfo = timezone(timedelta(minutes=tag.committer.offset))
                tagger_time = datetime.fromtimestamp(float(tag.committer.time), tagger_tzinfo)
                tagger = Contributor(tag.committer.name, tag.committer.email)
                release = Release(
                    version=version,
                    timestamp=tagger_time,
                    head=head,
                    author=tagger
                )
                graph.add(release)

            # Annotatted Tag
            elif tag.type == pygit2.GIT_OBJECT_TAG:
                peel = tag_ref.peel()
                # A tag may point to other objects in the repository
                # but we are only looking for tags that reference a commit
                if peel.type == pygit2.GIT_OBJECT_COMMIT:
                    head = self.git.get(peel.id)
                    try:
                        message = tag.message
                    except:
                        message = ''

                    if tag.tagger:
                        tagger = Contributor(tag.tagger.name, tag.tagger.email)
                        tagger_time_tzinfo = timezone(timedelta(minutes=tag.tagger.offset))
                        tagger_time = datetime.fromtimestamp(float(tag.tagger.time), tagger_time_tzinfo)
                    else:
                        tagger = Contributor(tag.committer.name, tag.committer.email)
                        tagger_time_tzinfo = timezone(timedelta(minutes=tag.committer.offset))
                        tagger_time = datetime.fromtimestamp(float(tag.committer.time), tagger_time_tzinfo)

                    release = Release(
                        version=version,
                        timestamp=tagger_time,
                        head=head,
                        author=tagger
                    )
                    graph.add(release)
