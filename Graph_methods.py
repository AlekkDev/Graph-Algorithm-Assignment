class Vertex:
    def __init__(self, id):
        self.id = id
        self.indegree = 0
        self.outdegree = 0
        self.edges = []  # list of  neighbor vertices

    def add_edge(self, target):
        if target not in self.edges and self.outdegree < 2:
            self.edges.append(target)
            self.outdegree += 1
            target.indegree += 1
            return True
        return False
    def remove_edge(self, target):
        if target in self.edges:
            self.edges.remove(target)
            self.outdegree -= 1
            target.indegree -= 1
            return True
        return False
    def is_disconnected(self):
        if self.indegree == 0 and self.outdegree == 0:
            return True
        return False
class Graph:
    def __init__(self, num_of_vertices):
        self.vertices = {i: Vertex(i) for i in range(num_of_vertices)}

    def add_edge(self, source_id, target_id):
        if source_id not in self.vertices or target_id not in self.vertices:
            return False
        source = self.vertices[source_id]
        target = self.vertices[target_id]
        return source.add_edge(target)

    def remove_edge(self, source_id, target_id):
        if source_id not in self.vertices or target_id not in self.vertices:
            return False
        source = self.vertices[source_id]
        target = self.vertices[target_id]
        return source.remove_edge(target)

    def unconnected_vertices(self):
        return [vertex.id for vertex in self.vertices.values() if vertex.is_disconnected()]

    def display_graph(self):
        for vertex in self.vertices.values():
            edges = [v.id for v in vertex.edges]
            print(f"Vertex {vertex.id}: Edges -> {edges}")
        print("All vertices in graph:", list(self.vertices.keys()))


# TODO Test script

def test_vertex():
    v0 = Vertex(0)
    v1 = Vertex(1)
    v2 = Vertex(2)
    v3 = Vertex(3)

    # Test adding edges
    assert v1.add_edge(v2)
    assert v1.add_edge(v3)
    assert v1.edges == [v2, v3]  # v1 should have edges to v2 and v3
    assert not v1.add_edge(v3)
    assert not v1.add_edge(v1)  # should not allow more than 2 outdegree edges

    assert v2.indegree == 1  # v2 should have 1 as indegree
    assert v1.outdegree == 2  # v1 should have 2 as outdegree

    # Test removing edges
    assert v1.remove_edge(v3)  # should remove edge from v1 to v3
    assert v1.outdegree == 1  # v1 outdegree should be 1 after removal"
    assert v3.indegree == 0  # v3 indegree should be 0 after edge removal"

    print("Vertex operations tests passed.")



def test_graph():
    graph = Graph(5)
    # graph.display_graph()
    print(graph.vertices)

    # Test adding edges
    assert graph.add_edge(0, 1)
    assert graph.add_edge(1, 2)
    assert graph.add_edge(2, 3)
    assert graph.add_edge(3, 4)  # Should allow adding edge
    assert not graph.add_edge(1, 2)  # Should not allow adding duplicate edge

    # Test removing edges
    assert graph.remove_edge(3, 4)  # should remove edge
    assert not graph.remove_edge(5, 1)  # can't remove edge that does not exist
    graph.display_graph()

    # Test checking disconnected vertices
    disconnected = graph.unconnected_vertices()
    assert 4 in disconnected, f"Expected vertex 4 to be disconnected, got {disconnected}"
    print("Graph operations tests passed.")