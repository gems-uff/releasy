
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import pygit2
import json

from releasy.commit import Commit
from releasy.contributor import Contributor
from releasy.graph import ProjectGraph, ReleaseGraph
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
        project = ProjectGraph()
        config = self.config
        for plugin in self.config.plugins:
            project = plugin.mine(project, config)
        return project


class MinerPlugin(ABC):
    @abstractmethod
    def mine(self, project: ProjectGraph, config: Configuration) -> ProjectGraph:
        pass
    

class JsonMiner(MinerPlugin):
    def __init__(self, json: Dict):
        self.json = json


    def mine(self, project: ProjectGraph, config: Configuration):
        project = self._mine_releases(project, config)
        project = self._mine_commits(project, config)
        return project
    

    def _mine_releases(self, project: ProjectGraph, config: Configuration):
        if 'releases' not in self.json:
            return project 

        #TODO parser from config
        parser = config.parser
        for release_data in self.json['releases']:
            version= parser.parse(release_data['name'])
            timestamp = release_data['timestamp']
            contributor = Contributor(release_data['name'])
            release = Release(
                version=version,
                timestamp=timestamp,
                head=release_data['head'],
                author=contributor
            )
            project.releases.add(release)
        return project

        
    def _mine_commits(self, project: ProjectGraph, config: Configuration):
        if 'commits' not in self.json:
            return project 
            
        for commit_data in self.json['commits']:
            commit_id = commit_data['id']
            timestamp = commit_data['timestamp']
            project.commits.add(Commit(commit_id, [], timestamp))

        for commit_data in self.json['commits']:
            if 'parents' not in commit_data:
                continue

            commit_id = commit_data['id']
            commit_node = project.commits[commit_id]
            for parent_id in commit_data['parents']:
                parent_node = project.commits[parent_id]
                commit_node.parents.append(parent_node)

        return project


class GitMiner(MinerPlugin):
    def __init__(self, path: str, mine_commits: bool = True):
        self.path = path
        self.git = pygit2.Repository(self.path) 
        self.mine_commits = mine_commits

    def mine(self, project: ProjectGraph, config: Configuration):
        self.fetch_tags(project, config)
        self.fetch_commits(project, config)
        return project
    
    def fetch_tags(self, project: ProjectGraph, config: Configuration) -> None:
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
                project.releases.add(release)

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
                    project.releases.add(release)

    def fetch_commits(self, project: ProjectGraph, config: Configuration) -> None:
        pass