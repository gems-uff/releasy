


from typing import Set
from releasy.commit import Commit, CommitNode
from releasy.miner import Configuration, Miner, MinerPlugin
from releasy.project import ProjectGraph
from releasy.release import Release


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

        for release in releases:
            head_node = project.commits[release.get().head]
            release_commits = list[CommitNode]()
            commit_stack = list[CommitNode]()

            commit_stack.append(head_node)
            while commit_stack:
                commit_node = commit_stack.pop()

                if commit_node in visited:
                    continue

                visited.add(commit_node)
                release.commits.add(commit_node.get())

                for parent_node in commit_node.parents:
                    commit_stack.append(parent_node)



                

        

        return project
    
    