from typing import List
from releasy.release import Release


class GraphNode[T]:
    def __init__(self, ref: T):
        self.ref = ref
        self.prev_refs = []


class Graph[T]:
    def __init__(self):
        self.nodes = dict[str, GraphNode]()

    def add(self, ref: T, prev_refs: List[T] = None) -> None:
        if not prev_refs:
            prev_refs = []

        name = self._ref_name(ref)
        if name in self.nodes:
            node = self.nodes[name]
        else:
            node = GraphNode(ref)
            self.nodes[name] = node

        for prev_ref in prev_refs:
            prev_node = GraphNode(prev_ref) 
            node.prev_refs.append(prev_node)

    
    def get(self, name: str):
        node = self.nodes[name]
        return node.ref
    
    def __getitem__(self, obj):
        if isinstance(obj, str):
            name = obj
        elif isinstance(obj, T):
            name = self._ref_name(obj)
        else:
            return None

        return self.get(name)

    def previous(self, ref) -> List[T]:
        name = self._ref_name(ref)
        node = self._get_node(name)
        return [node.ref for node in node.prev_refs]

    def _get_node(self, name: str):
        node = self.nodes[name]
        return node

    def __len__(self) -> int:
        return len(self.nodes)
    
    def _ref_name(self, ref: T):
        pass


class ReleaseGraph(Graph[Release]):
    def __init__(self):
        super().__init__()

    def _ref_name(self, ref: Release):
        return ref.name


