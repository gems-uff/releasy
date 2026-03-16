from datetime import datetime
from typing import Dict, Optional

from releasy.configuration import Configuration
from releasy.models.commit import Commit
from releasy.models.contributor import Contributor
from releasy.models.release import Release
from releasy.miners.miner import MinerPlugin


class JsonMiner(MinerPlugin):
    def __init__(self, json: Dict, config: Optional[Configuration] = None):
        super().__init__(config)
        self.json = json

    def mine(self, project):
        if self.config is None:
            raise ValueError("JsonMiner configuration has not been set")

        project = self._mine_commits(project)
        project = self._mine_releases(project)
        return project

    def _mine_releases(self, project):
        if 'releases' not in self.json:
            return project 

        parser = self.config.version_format
        for release_data in self.json['releases']:
            if not parser.parse(release_data['name']):
                continue
            timestamp = datetime.fromisoformat(release_data['timestamp'])
            contributor = Contributor(release_data.get('author', release_data['name']))
            head_id = release_data['head']
            head = project.commits[head_id]
            release = Release(
                name=release_data['name'],
                timestamp=timestamp,
                head=head,
                author=contributor,
                version_format=self.config.version_format,
            )
            project.releases.append(release)
        return project

    def _mine_commits(self, project):
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
