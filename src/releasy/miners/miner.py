
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import pygit2
import json

from releasy.models.commit import Commit
from releasy.models.contributor import Contributor
from releasy.version_format import ReleaseVersionFormat, SemanticVersioningFormat
from releasy.models.project import Project
from releasy.models.release import Release


@dataclass
class Configuration:
    plugins: List[str]
    parser: ReleaseVersionFormat = SemanticVersioningFormat()


class Miner:
    def __init__(self, config: Configuration) -> None:
        self.config = config

    def mine(self):
        project = Project()
        config = self.config
        for plugin in self.config.plugins:
            project = plugin.mine(project, config)
        return project


class MinerPlugin(ABC):
    @abstractmethod
    def mine(self, project: Project, config: Configuration):
        pass
    

class JsonMiner(MinerPlugin):
    def __init__(self, json: Dict):
        self.json = json


    def mine(self, project: Project, config: Configuration):
        project = self._mine_commits(project, config)
        project = self._mine_releases(project, config)
        return project
    

    def _mine_releases(self, project: Project, config: Configuration):
        if 'releases' not in self.json:
            return project 

        #TODO parser from config
        parser = config.parser
        for release_data in self.json['releases']:
            version = parser.parse(release_data['name'])
            timestamp = datetime.fromisoformat(release_data['timestamp'])
            contributor = Contributor(release_data.get('author', release_data['name']))
            head_id = release_data['head']
            head = project.commits[head_id]
            release = Release(
                name=release_data['name'],
                timestamp=timestamp,
                head=head,
                author=contributor
            )
            release.version = version
            project.releases.append(release)
        return project

        
    def _mine_commits(self, project: Project, config: Configuration):
        if 'commits' not in self.json:
            return project 
            
        for commit_data in self.json['commits']:
            commit_id = commit_data['id']
            timestamp = datetime.fromisoformat(commit_data['timestamp'])
            project.commits.append(Commit(id=commit_id, committer_time=timestamp))

        for commit_data in self.json['commits']:
            if 'parents' not in commit_data:
                continue

            commit_id = commit_data['id']
            commit = project.commits[commit_id]
            for parent_id in commit_data['parents']:
                parent = project.commits[parent_id]
                commit.add_parent(parent)

        return project


class GitMiner(MinerPlugin):
    def __init__(self, path: str, mine_commits: bool = True):
        self.path = path
        self.git = pygit2.Repository(self.path) 
        self.mine_commits = mine_commits


    def mine(self, project: Project, config: Configuration):
        self.fetch_tags(project, config)
        self.fetch_commits(project, config)
        return project

    
    def fetch_tags(self, project: Project, config: Configuration) -> None:
        tag_refs = [
            ref 
            for ref in self.git.references.objects 
            if ref.name.startswith('refs/tags/')
        ]
        version_parser = config.parser

        for tag_ref in tag_refs:
            tag = self.git.get(tag_ref.target)
            release_name = tag_ref.shorthand

            version = version_parser.parse(release_name)
            if not version:
                continue

            # Simple Tag
            if tag.type == pygit2.GIT_OBJECT_COMMIT:
                head = Commit(id=str(tag.id))
                author = None
                tagger_tzinfo = timezone(timedelta(minutes=tag.committer.offset))
                tagger_time = datetime.fromtimestamp(float(tag.committer.time), tagger_tzinfo)
                tagger = Contributor(tag.committer.name, tag.committer.email)
                release = Release(
                    name=release_name,
                    timestamp=tagger_time,
                    head=head,
                    author=tagger
                )
                release.version = version
                project.releases.append(release)

            # Annotatted Tag
            elif tag.type == pygit2.GIT_OBJECT_TAG:
                peel = tag_ref.peel()
                # A tag may point to other objects in the repository
                # but we are only looking for tags that reference a commit
                if peel.type == pygit2.GIT_OBJECT_COMMIT:
                    head = Commit(id=str(peel.id))
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
                        name=release_name,
                        timestamp=tagger_time,
                        head=head,
                        author=tagger,
                        message=message,
                    )
                    release.version = version
                    project.releases.append(release)


    def fetch_commits(self, project: Project, config: Configuration) -> None:
        pass
