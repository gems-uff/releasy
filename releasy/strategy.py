


from collections import defaultdict
from typing import Set
from releasy.commit import Commit, CommitNode
from releasy.miner import Configuration, Miner, MinerPlugin
from releasy.project import ProjectGraph
from releasy.release import Release, ReleaseNode


# class ReferenceReleaseStrategy:
#     def __init__(self, version_format: ReleaseVersionFormat) -> None:
#         self.version_format = version_format

#     def assign(self, repository: Repository, releases: Set[Release] = None) -> Set[Release]:
#         releases = list[Release]()

#         for (name, head, author, timestamp) in repository.release_refs():
#             version = self.version_format.parse(name)
#             if not version:
#                 continue

#             release = Release(version, timestamp, None, author)
#             releases.append(release)

#         return releases

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
    

#TODO Change from miner to another super class that need a previous mined project
class BasedReleaseStrategy(MinerPlugin):
    def mine(self, project: ProjectGraph, config: Configuration):
        releases = [release_node for release_node in project.releases.get_all()]

        for release_node in releases: 
            base_release_nodes = set[ReleaseNode]()
            for tail_node in release_node.tails:
                for parent_node in tail_node.parents:
                    base_release_nodes = \
                        (base_release_nodes | project.releases.get_from_commit(parent_node)) \
                        - set([release_node])
            release_node.base_releases = base_release_nodes

        return project
