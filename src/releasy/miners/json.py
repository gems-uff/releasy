from datetime import datetime
from typing import Dict

from releasy.models.commit import Commit
from releasy.models.contributor import Contributor
from releasy.models.release import Release
from releasy.miners.miner import Configuration, MinerPlugin


class JsonMiner(MinerPlugin):
    def __init__(self, json: Dict):
        self.json = json

    def mine(self, project, config: Configuration):
        project = self._mine_commits(project, config)
        project = self._mine_releases(project, config)
        return project

    def _mine_releases(self, project, config: Configuration):
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

    def _mine_commits(self, project, config: Configuration):
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
