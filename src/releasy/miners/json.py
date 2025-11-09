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
            contributor = Contributor(release_data['name'])
            head_id = release_data['head']
            head = project.commits[head_id].get()
            release = Release(
                version=version,
                timestamp=timestamp,
                head=head,
                author=contributor
            )
            project.releases.add(release)
        return project

    def _mine_commits(self, project, config: Configuration):
        if 'commits' not in self.json:
            return project 
            
        for commit_data in self.json['commits']:
            commit_id = commit_data['id']
            timestamp = datetime.fromisoformat(commit_data['timestamp'])
            project.commits.add(Commit(commit_id, timestamp))

        for commit_data in self.json['commits']:
            if 'parents' not in commit_data:
                continue

            commit_id = commit_data['id']
            commit_node = project.commits[commit_id]
            for parent_id in commit_data['parents']:
                parent_node = project.commits[parent_id]
                commit_node.parents.append(parent_node)

        return project
