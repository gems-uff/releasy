from dataclasses import dataclass
from queue import Queue
from typing import List
from releasy.commit import Commit
from releasy.release import Release


class GraphNode[T]:
    def __init__(self, ref: T):
        self.ref = ref
        self.parents = []
    
    def add_parent(self, parent):
        self.parents.append(parent)
    
    def __repr__(self):
        return self.ref.__repr__()
    

class Graph[T]:
    def __init__(self, ref_name, check_type):
        self.nodes = dict[str, GraphNode]()
        self._ref_name = ref_name
        self._check_type = check_type

    def _add_node(self, ref: T):
        name = self._ref_name(ref) 
        if name in self.nodes:
            node = self.nodes[name]
        else:
            node = GraphNode(ref)
            self.nodes[name] = node
        return node
    
    def _add_edge(self, node: GraphNode, parent: GraphNode):
        node.add_parent(parent)

    def _get_node(self, ref: str | T):
        if isinstance(ref, str):
            name = ref
        elif self._check_type(ref):
            name = self._ref_name(ref)
        else:
            return None
        
        if name not in self.nodes:
            return None
        
        node = self.nodes[name]
        return node

    def add(self, ref: T, parents_ref: List[T] = None) -> None:
        if not parents_ref:
            parents_ref = []

        node = self._add_node(ref)
        for parent_ref in parents_ref:
            parent_node = self._add_node(parent_ref)
            self._add_edge(node, parent_node)
    
    def get(self, ref: str | T):
        node = self._get_node(ref)
        if not node:
            return None
        
        ref = node.ref
        return ref
    
    def get_all(self) -> T:
        releases = [release.ref for release in self.nodes.values()]
        return releases
    
    def __getitem__(self, ref: str | T):
        return self.get(ref)

    def get_parents(self, ref: str | T) -> List[T]:
        node = self._get_node(ref)
        parents_ref = [node.ref for node in node.parents]
        return parents_ref
    
    def get_path(self, target: str | T, origin: str | T):
        target = self._get_node(target)
        origin = self._get_node(origin)

        queue = Queue[GraphNode]()
        queue.put(origin)
        origin_of = dict()
        while not queue.empty():
            current = queue.get()

            if current == target:
                break

            for parent in current.parents:
                if parent not in origin_of:
                    origin_of[parent] = current
                    queue.put(parent)

        path = []
        current = target

        if current not in origin_of:
            return path

        while current != origin:
            current = origin_of[current]
            path.insert(0, current)
        path.append(target)
        path = [node.ref for node in path]
        return path

    def reach(self, target: str | T, origin: str | T):
        path = self.get_path(target, origin)
        return True if path else False

    def __len__(self) -> int:
        return len(self.nodes)
    

class ReleaseGraph(Graph[Release]):
    def __init__(self):
        super().__init__(
            lambda release: release.name,
            lambda release: isinstance(release, Release)
        )
        self.commits = dict[str, list[Commit]]()

    def add_commit(self, release, commits: list[Commit]):
        if release not in self.commits:
            self.commits[release.name] = list()
            
        commits = self.commits[release.name]
        for commit in commits:
            commits.append[commit]

    #TODO: move to a inspector class to remove business logic
    def get_main_parent(self, ref: str | Release) -> Release:
        releases = self.get_parents(ref)
        if not releases:
            return None
            
        ref = self.get(ref)
        releases.append(ref)
        releases = sorted(releases, key=lambda r: r.version)
        pos = releases.index(ref)
        if pos > 0:
            return releases[pos-1]
            
        releases = sorted(releases, key=lambda r: r.version)
        pos = releases.index(ref)
        return releases[1]


class CommitGraph(Graph[Commit]):
    def __init__(self):
        super().__init__(
            lambda commit: commit.id,
            lambda commit: isinstance(commit, Commit)
        )


class ReleaseNode:
    def __init__(self, release: Release):
        self.release = release
        self.base_releases = list[Release]()
        self.commits = list[CommitNode]()

    def get(self) -> Release:
        return self.release

    def add_commit(self, commits: List[Commit]):
        self.commits.extend(CommitNode(commit) for commit in commits)


Reference = Release | Commit


class CommitNode:
    def __init__(self, commit: Commit):
        self.commit = commit
        self.parents = list[CommitNode]
    
    def get(self) -> Commit:
        return self.commit


class RGraph:
    def __init__(self):
        self.nodes = dict[str, ReleaseNode]()
  
    def add(self, release: Release):
        if release.name not in self.nodes:
            release_node = ReleaseNode(release)
            self.nodes[release.name] = release_node
    
    def get(self, reference: str) -> ReleaseNode:
        if reference not in self.nodes:
            return None
        return self.nodes[reference]
    
    def get_all(self) -> List[ReleaseNode]:
        release_nodes = [release_node for release_node in self.nodes.values()]
        return release_nodes

    def __getitem__(self, reference: str | Release):
        if isinstance(reference, Release):
            return self.get(reference.name)
        return self.get(reference)
    
    def __len__(self) -> int:
        return len(self.nodes)

class ProjectGraph:
    def __init__(self):
        self.releases = RGraph()
        # self.commits = CommitGraph()

    # def add_release(self, release: Release):
    #     self.releases.add(release)

    # def add_release_commit(self, release: Release, commits: List[Commit]):
    #     self.releases.add_commits(release, commits)

# class ReleaseCommitGraph:
#     def __init__(self):
#        self.commits = Graph[Commit]()

#TODO rename to ReleaseGraph
# class RelGraph:
#     def __init__(self):
#        self.releases = ReleaseCommitGraph()
#        self.commits = Graph[Commit]()
        
# class CommitGraph(Graph[Commit]):
#     def __init__(self):
#         super().__init__(
#             lambda commit: commit.id,
#             lambda commit: isinstance(commit, Commit)
#         )


# class ProjectGraph:
#     def __init__(self):
#         self.releases: Graph[Release] = None
#         self.commits: Graph[Commit] = None

        
        # graph.release['1.0.0']  -> Get release
        # graph.release['1.0.0'].commits -> Get commits from release
        # graph.commits['ab10'] -> Get commits


