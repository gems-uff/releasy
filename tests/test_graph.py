

# from releasy.release import Release


# class DescribeReleaseGraph:
#     def it_add_release(self, release_a: Release):
#         graph = RRGraph()
#         assert(len(graph) == 0)

#         graph.add(release_a)
#         assert(len(graph) == 1)

#     def it_retrieve_release_by_name(self, release_a: Release):
#         graph = RRGraph()
#         graph.add(release_a)

#         release = graph[release_a.name]
#         assert release == release_a

#         release = graph.get(release_a.name)
#         assert release == release_a
    
#     def it_retrieve_release_by_ref(self, release_a: Release):
#         graph = RRGraph()
#         graph.add(release_a)

#         release = graph[release_a]
#         assert release == release_a

#         release = graph.get(release_a)
#         assert release == release_a

#     def it_track_parent_releases(self, release_a, release_b, release_c):
#         graph = RRGraph()
#         graph.add(release_a)
#         graph.add(release_b)
#         graph.add(release_c, [release_a, release_b])
#         assert(len(graph) == 3)

#         bse_rleases = graph.get_parents(release_c)
#         assert len(bse_rleases) == 2
#         assert bse_rleases[0] == release_a
#         assert bse_rleases[1] == release_b
        
#         graph = RRGraph()
#         graph.add(release_a)
#         graph.add(release_b)
#         graph.add(release_c, [release_a])
#         graph.add(release_c, [release_b])
#         assert(len(graph) == 3)

#         bse_rleases = graph.get_parents(release_c)
#         assert len(bse_rleases) == 2
#         assert bse_rleases[0] == release_a
#         assert bse_rleases[1] == release_b
    
#     def it_track_main_parent(self, release_a, release_b, release_c):
#         graph = RRGraph()
#         graph.add(release_c, [release_a, release_b])
#         main_parent = graph.get_main_parent(release_c)
#         assert main_parent == release_b

#         graph = RRGraph()
#         graph.add(release_a, [release_b, release_c])
#         main_parent = graph.get_main_parent(release_a)
#         assert main_parent == release_b
    
#     def it_track_path_between_releases(self, release_a, release_b, release_c):
#         graph = RRGraph()
#         graph.add(release_a)
#         graph.add(release_b, [release_a])
#         graph.add(release_c, [release_b])

#         assert [release_b, release_a] == \
#             graph.get_path(release_a, origin=release_b)
#         assert [release_c, release_b, release_a] == \
#             graph.get_path(release_a, origin=release_c)
#         assert [release_c, release_b] == \
#             graph.get_path(release_b, origin=release_c)

#         graph = RRGraph()
#         graph.add(release_a)
#         graph.add(release_b, [release_a])
#         graph.add(release_c, [release_a])
#         assert [] == \
#             graph.get_path(release_b, origin=release_c)
        
#     def it_track_reach_between_releases(self, release_a, release_b, release_c):
#         graph = RRGraph()
#         graph.add(release_a)
#         graph.add(release_b, [release_a])
#         graph.add(release_c, [release_b])

#         assert graph.reach(release_a, origin=release_b)
#         assert graph.reach(release_a, origin=release_c)
#         assert graph.reach(release_b, origin=release_c)

#         graph = RRGraph()
#         graph.add(release_a)
#         graph.add(release_b, [release_a])
#         graph.add(release_c, [release_a])
#         assert not graph.reach(release_b, origin=release_c)
    

# class DescribeProjectGraph:
#     def it_add_release(self, release_a: Release):
#         project = ProjectGraph()
#         assert len(project.releases) == 0

#         project.releases.add(release_a)
#         assert len(project.releases) == 1
#         assert release_a == project.releases[release_a].get()

#     def it_add_commit_to_release(self, release_a: Release, commit_a, commit_b):
#         project = ProjectGraph()
#         project.releases.add(release_a)
#         project.releases[release_a].commits.add(commit_a)
#         project.releases[release_a].commits.add(commit_b)

#         assert len(project.releases) == 1
#         commits = project.releases[release_a.name].commits
#         assert len(commits) == 2
#         assert commit_a  == commits['A'].get()
#         assert commit_b  == commits['B'].get()

    