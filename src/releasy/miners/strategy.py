


from collections import defaultdict
from releasy.models.commit import Commit
from releasy.miners.miner import Configuration, Miner, MinerPlugin
from releasy.models.release import Release


#TODO Change from miner to another super class that need a previous mined project
class HistoryBasedStrategy(MinerPlugin):
    def mine(self, project, config: Configuration):
        releases = sorted(project.releases, key=lambda r: r.timestamp)
        visited = set[Commit]()
        commit2release = defaultdict(set)

        for release in releases:
            head = project.commits[release.head.id]
            commit_stack = list[Commit]()
            base_releases = set[Release]()

            release.commits = type(release.commits)()
            release.base_releases = type(release.base_releases)()

            commit_stack.append(head)
            while commit_stack:
                commit = commit_stack.pop()

                if commit in visited:
                    base_releases = (base_releases | commit2release[commit]) - set([release])
                    continue

                visited.add(commit)
                release.commits.append(commit)
                commit2release[commit].add(release)

                try:
                    parents = commit.parents
                except ValueError:
                    parents = []

                for parent in parents:
                    commit_stack.append(parent)
            
            for base_release in base_releases:
                release.add_base_release(base_release)

        return project
    
