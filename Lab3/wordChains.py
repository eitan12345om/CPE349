import json
import queue
import sys


class Dijkstra():
    def __init__(self, graph):
        """Initializes Dijkstra class

        Arguments:
            graph {dict} -- The graph used for Dijkstra's algorithm
        """
        self.graph = graph
        self.vertices = []

    def dijkstras_algorithm(self, startWord, endWord):
        """Performs Dijkstra's Algorithm.

        Uses Dijkstra's Algorithm to find the shortest path from startWord
        to endWord. This algorithm is optimized by stopping as soon as
        endWord is reached.

        Arguments:
            startWord {str} -- The word to start from
            endWord {str} -- The word to find the path to

        Returns:
            Vertex -- The vertex containing the endWord with the shortest path
        """
        def relax_vertex(vertex, neighbor):
            """Relaxes neighboring vertex

            Inner method which checks if neighbor is closer than previously
            thought. If so, update information--distance and parent.

            Arguments:
                vertex {Vertex} -- Vertex currently at
                neighbor {Vertex} -- Neighbor of vertex
            """
            if vertex.distance + 1 < neighbor.distance:
                neighbor.distance = vertex.distance + 1
                neighbor.parent = vertex

        self.init_vertices()
        my_queue = queue.Queue()

        vertex = self.find_vertex_from_word(startWord)
        vertex.distance = 0

        my_queue.put(vertex)

        while not my_queue.empty():
            vertex = my_queue.get()
            vertex.finished = True

            # Don't search further if found endWord
            if vertex.word == endWord:
                return vertex

            # Loop through unfinished neighbors and relax
            for neighbor in vertex.adjacency_list:
                neighbor = self.find_vertex_from_word(neighbor)
                if not neighbor.finished:
                    relax_vertex(vertex, neighbor)
                    my_queue.put(neighbor)

        return None

    def find_vertex_from_word(self, word):
        """Find a vertex from a word

        Loops through each vertex in self.vertices and returns the vertex
        with vertex.word == word. Otherwise returns None.

        Arguments:
            word {str} -- The word used to find the vertex

        Returns:
            Vertex -- The vertex matching the word
        """
        for vertex in self.vertices:
            if vertex.word == word:
                return vertex

        return None

    def init_vertices(self):
        """Initializes vertices in graph

        Creates a new Vertex and adds it to the vertices list
        """
        self.vertices = []
        for key in self.graph:
            self.vertices.append(self.Vertex(key, self.graph[key]))

    def path_to_stack(self, vertex):
        """Puts shortest path on stack

        Reverses shortest path calculated by dijkstra's by adding to stack

        Arguments:
            vertex {Vertex} -- Vertex containing endWord

        Returns:
            list -- Stack containing shortest path
        """
        stack = [vertex]

        while vertex.parent is not None:
            vertex = vertex.parent
            stack.append(vertex)

        return stack

    class Vertex():
        def __init__(self, word, adjacency_list):
            """Creates a new Vertex

            Creates a new vertex in preparation.
            The distance is set to infinity and parent is None

            Arguments:
                word {str} -- A word
                adjacency_list {dict} -- Dictionary of associated words
            """
            self.word = word
            self.adjacency_list = adjacency_list
            self.distance = float("inf")
            self.parent = None
            self.finished = False


def _check_usage(args):
    """Checks usage of program

    The first file should contain an undirected graph. The second file
    contains pairs of words split by newlines like so:

    drift, wood
    taco, bell

    Arguments:
        args {list} -- List of command line arguments
    """
    if len(args) != 3:
        sys.exit("Usage: python degrees.py <file> <file>")


def _write_shortest_path(stack, outFile):
    """Writes shortest path to outFile

    Arguments:
        stack {list} -- Stack containing shortest path starting from stack[0]
        outFile {FILE} -- File to write to
    """
    pathLength = len(stack)

    outFile.write(stack.pop().word)
    while len(stack) > 0:
        outFile.write(" --> %s" % stack.pop().word)
    outFile.write(", %d steps\n" % pathLength)


def main():
    _check_usage(sys.argv)

    with open(sys.argv[1], "r") as graphFile:
        graph = json.load(graphFile)

    dijkstra = Dijkstra(graph)

    with open(sys.argv[2], "r") as inFile:
        with open("shortest_paths.txt", "w") as outFile:
            for line in inFile:
                line = ''.join(line.split()).split(",")

                vertex = dijkstra.dijkstras_algorithm(line[0], line[1])
                if vertex is None:
                    outFile.write("No path from %s to %s\n" % (line[0],
                                  line[1]))

                stack = dijkstra.path_to_stack(vertex)
                _write_shortest_path(stack, outFile)


if __name__ == '__main__':
    main()
