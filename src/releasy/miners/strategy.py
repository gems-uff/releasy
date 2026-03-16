
from collections import defaultdict

from releasy.models.commit import Commit, CommitList
from releasy.miners.miner import MinerPlugin
from releasy.models.release import Release, ReleaseList


#TODO Change from miner to another super class that need a previous mined project
class HistoryBasedStrategy(MinerPlugin):
    def mine(self, project):
        releases = sorted(project.releases, key=lambda r: r.timestamp)
        visited = set[Commit]()
        commit2release = defaultdict(set)
        release_to_commit_ids: dict[Release, list[str]] = {}

        for release in releases:
            head = project.commits[release.head.id]
            commit_stack = list[Commit]()
            base_releases = set[Release]()
            assigned_commits: list[Commit] = []

            release.previous = ReleaseList()
            release.next = ReleaseList()

            commit_stack.append(head)
            while commit_stack:
                commit = commit_stack.pop()

                if commit in visited:
                    base_releases = (base_releases | commit2release[commit]) - set([release])
                    continue

                visited.add(commit)
                assigned_commits.append(commit)
                commit2release[commit].add(release)

                try:
                    parents = commit.parents
                except ValueError:
                    parents = []

                for parent in parents:
                    commit_stack.append(parent)
            
            for base_release in base_releases:
                release.add_previous(base_release)

            release_to_commit_ids[release] = [commit.id for commit in assigned_commits]

        for release, commit_ids in release_to_commit_ids.items():
            release.set_commits_loader(
                lambda ids=tuple(commit_ids): CommitList(
                    project.commits[commit_id]
                    for commit_id in ids
                )
            )

        return project
    
