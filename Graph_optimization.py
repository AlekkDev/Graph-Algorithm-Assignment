import random
from Graph_methods import Graph
from collections import deque
from math import log2

# This "algorithm" is inspired by bogosort as it randomly adds edges to graphs
# It has the same characteristics as bogosort, it is probably the least efficient way to optimize a graph,
# but it gets the job done eventually. In this case I used log2(n) where n is number of vertices in graph,
# to find the mathematically best possible structure of the graph so that the maximum distance between
# any two nodes is minimized. Essentially, the graph is optimized when the maximum distance is log2(n).
# I got log2(n) considering 2indegree and 2outdegree for each vertex
# The algorithm should eventually find the best possible solution
# The longer the code, the longer it takes to find the solution
# ex: For 45 vertices it takes about 15-20 seconds to find the best possible solution while <30 is almost instant


# BFS to calculate shortest path from some start node to all other nodes (but store all distances)
def bfs_distances(graph, start_node):  # Calculate distances from start node to all other nodes
    distances = {vertex_id: float('inf') for vertex_id in graph.vertices} # not having this breaks the code
    distances[start_node] = 0
    queue = deque([start_node])  # Initialize queue

    while queue:  # While queue is not empty
        current = queue.popleft()  # Get the current node
        current_distance = distances[current]  # Get the distance to the current node
        for neighbor in graph.vertices[current].edges:  # For each neighbor of the current node
            if distances[neighbor.id] == float('inf'):  # If the neighbor has not been visited
                distances[neighbor.id] = current_distance + 1  # Set the distance to the neighbor
                queue.append(neighbor.id)  # Add neighbor to the queue
    return distances

# Simple function to return the maximum distance between any two nodes in the graph
def return_max_distance(graph):
    max_distance = 0
    for vertex_id in graph.vertices:
        distances = bfs_distances(graph, vertex_id)
        max_distance = max(distances.values())
    return max_distance


def add_edges_random(graph): # Add random edges to the graph
    vertices = list(graph.vertices.values())  # Get all vertices in the graph
    max_attempts = 1000 # Maximum number of attempts to add edges

    for vertex in vertices:  # For each vertex
        attempt = 0
        while vertex.outdegree < 2 and attempt < max_attempts:  # While the vertex has less than 2 outgoing edges
            # Get potential targets (vertices that are not the current vertex and have less than 2 incoming edges)
            potential_targets = [v for v in vertices if v.id != vertex.id and v.indegree < 2]
            if not potential_targets: # If there are no potential targets, break
                break
            target = random.choice(potential_targets) # Choose random target
            vertex.add_edge(target) # Add edge from the current vertex to the target
            attempt += 1 # Increment attempt counter
        if vertex.outdegree < 2:
            print(f"Warning: Could not add enough edges from vertex {vertex.id} after {max_attempts} attempts.")

def is_satisfactory(graph):  # Check if the graph is well "interconnected"
    for vertex in graph.vertices.values():  # For each vertex
        # If the vertex has no incoming or outgoing edges, or the maximum distance is greater than 7
        if vertex.indegree < 1 or vertex.outdegree < 1: #
            return False
    return True

def shuffle_graph(graph): # Shuffle the graph
    for vertex in graph.vertices.values(): # For each vertex
        while vertex.edges:
            target = vertex.edges[0] # Get the first target
            vertex.remove_edge(target)   # Remove edge from vertex to target

def optimize_graph_randomly(graph):
    add_edges_random(graph)  # Add random edges to graph
    while not is_satisfactory(graph):  # While the graph is not satisfactory
        print("Reshuffling graph...")
        shuffle_graph(graph)  # Shuffle the graph
        add_edges_random(graph)  # Add random edges to graph again
    distances = return_max_distance(graph)
    n = len(graph.vertices)
    while distances >log2(n): # if max distance is not the best possible, reshuffle and try again
        shuffle_graph(graph)
        add_edges_random(graph)
        distances = return_max_distance(graph)
    return graph

#TODO TESTING CODE

graph = Graph(16) # Solution is instant, the higher the number of vertices, the longer it takes to find the solution
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(4, 3)
graph.add_edge(8, 4)
print("Initial graph:")
graph.display_graph()

optimized_graph = optimize_graph_randomly(graph)

print("Optimized graph:")
optimized_graph.display_graph()
print("Max distance is", return_max_distance(optimized_graph))
# print("Max distance in graph:", max(bfs_distances(graph, 0).values()))