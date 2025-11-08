


from collections import defaultdict
from typing import Set
from releasy.models.commit import Commit, CommitNode
from releasy.miners.miner import Configuration, Miner, MinerPlugin
from releasy.models.project import ProjectGraph
from releasy.models.release import Release, ReleaseNode


#TODO Change from miner to another super class that need a previous mined project
class HistoryBasedStrategy(MinerPlugin):
    def mine(self, project: ProjectGraph, config: Configuration):
        releases = [release_node for release_node in project.releases.get_all()]
        releases = sorted(releases, key=lambda r: r.get().timestamp)
        visited = set[CommitNode]()
        # commit2release = defaultdict[Commit, set(Release)](set[Release])
        commit2release = defaultdict(set)

        for release_node in releases:
            head_node = project.commits[release_node.get().head]
            release_commits = list[CommitNode]()
            commit_stack = list[CommitNode]()
            base_release_nodes = set[ReleaseNode]()

            commit_stack.append(head_node)
            while commit_stack:
                commit_node = commit_stack.pop()

                if commit_node in visited:
                    base_release_nodes = \
                        (base_release_nodes | commit2release[commit_node]) \
                        - set([release_node])
                    #TODO tail
                    continue

                visited.add(commit_node)
                release_node.commits.add(commit_node.get())
                commit2release[commit_node].add(release_node)

                for parent_node in commit_node.parents:
                    commit_stack.append(parent_node)
            
            release_node.base_releases = list(base_release_nodes)

        return project
    
