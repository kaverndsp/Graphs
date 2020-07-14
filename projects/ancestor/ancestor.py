# Understand
# Plan
# Use a BFS to get every parent child / child to parent relationship. Not every child has a parent, so we need to use BFS to get all child parent relationships before attempting to find the earliest ancestor
class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        self.vertices[v1].add(v2)


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def earliest_ancestor(ancestors, starting_node):
    graph = Graph()

    for pair in ancestors:
        graph.add_vertex(pair[0])
        graph.add_vertex(pair[1])
        graph.add_edge(pair[1], pair[0])

    q = Queue()
    q.enqueue([starting_node])

    longest_path_length = 0
    earliest_ancestor = starting_node

    while q.size():

        path = q.dequeue()
        current_node = path[-1]

        if len(path) > longest_path_length:
            longest_path_length = len(path)
            earliest_ancestor = current_node

        neighbors = graph.vertices[current_node]

        for neighbor in neighbors:

            path_copy = list(path)
            path_copy.append(neighbor)
            q.enqueue(path_copy)

    return path[-1]
