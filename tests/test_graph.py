

from releasy.graph import ReleaseGraph
from releasy.release import Release


class DescribeReleaseGraph:
    def it_add_release(self, release_a: Release):
        graph = ReleaseGraph()
        assert(len(graph) == 0)

        graph.add(release_a)
        assert(len(graph) == 1)

    def it_retrieve_release_by_name(self, release_a: Release):
        graph = ReleaseGraph()
        graph.add(release_a)

        release = graph[release_a.name]
        assert release == release_a

        release = graph.get(release_a.name)
        assert release == release_a

    def it_track_dependency(self, release_a, release_b):
        graph = ReleaseGraph()
        graph.add(release_a)
        graph.add(release_b, [release_a])
        assert(len(graph) == 2)

        bse_rleases = graph.previous(release_a)
        assert len(bse_rleases) == 0

        bse_rleases = graph.previous(release_b)
        assert len(bse_rleases) == 1
        assert bse_rleases[0] == release_a

    def it_track_mul_dep(self, release_a, release_b, release_c):
        graph = ReleaseGraph()
        graph.add(release_a)
        graph.add(release_b)
        graph.add(release_c, [release_a, release_b])
        assert(len(graph) == 3)

        bse_rleases = graph.previous(release_c)
        assert len(bse_rleases) == 2
        assert bse_rleases[0] == release_a
        assert bse_rleases[1] == release_b
        
    def it_track_mul_dep_2(self, release_a, release_b, release_c):
        graph = ReleaseGraph()
        graph.add(release_a)
        graph.add(release_b)
        graph.add(release_c, [release_a])
        graph.add(release_c, [release_b])
        assert(len(graph) == 3)

        bse_rleases = graph.previous(release_c)
        assert len(bse_rleases) == 2
        assert bse_rleases[0] == release_a
        assert bse_rleases[1] == release_b
    
    def it_handle_loops(self, release_a, release_b, release_c):
        graph = ReleaseGraph()
        graph.add(release_a)
        graph.add(release_b, [release_a])
        graph.add(release_c, [release_b]) 
        graph.add(release_a, [release_c]) 











