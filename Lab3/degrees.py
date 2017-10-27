import json
import sys


class Degree():
    """Calculates frequencies of vertices"""
    def __init__(self):
        pass

    def __calculate_frequency(self, graph, numEdges):
        """Calculates the frequency of vertices in a graph

        Arguments:
            graph {dict} -- The graph for which to calculate the frequency
            numEdges {int} -- The number of edges in the graph

        Returns:
            dict -- Frequency distribution of the graph's vertices
        """
        frequencies = {}

        for key in graph:
            total = 0
            for word in graph[key]:
                total += graph[key][word]

            frequencies[key] = {total: total / numEdges}

        return frequencies

    def __count_edges(self, graph, directed=False):
        """Counts the number of edges in a graph

        Arguments:
            graph {dict} -- Graph for which to count the edges

        Keyword Arguments:
            directed {bool} -- Whether graph is directed (default: {False})

        Returns:
            int -- The total number of edges in the graph
        """
        total = 0

        for key in graph:
            for word in graph[key]:
                total += graph[key][word]

        return total if directed else total / 2

    def __write_to_JSON(self, frequencies, outName):
        """Writes frequencies to JSON file

        Arguments:
            frequencies {dict} -- Frequency of vertex distribution
            outName {str} -- Name of file
        """
        with open(outName, "w") as outFile:
            json.dump(frequencies, outFile, indent=4, sort_keys=True)

    def directed_vertex_distribution(self, fname,
                                     indegree="indegree_histogram.json",
                                     outdegree="outdegree_histogram.json"):
        """Calculates and outputs indegree and outdegree frequencies

        Arguments:
            fname {str} -- Input file containing graph

        Keyword Arguments:
            indegree {str} -- Output file for indegree histogram
            (default: {"indegree_histogram.json"})
            outdegree {str} -- Output file for outdegree histogram
            (default: {"outdegree_histogram.json"})
        """
        with open(fname, "r") as inFile:
            graph = json.load(inFile)

        numEdges = self.__count_edges(graph, directed=True)
        out_frequencies = self.__calculate_frequency(graph, numEdges)
        self.__write_to_JSON(out_frequencies, outdegree)

        in_frequencies = {}
        for key in self.undirected_graph:
            total = 0
            for word in self.undirected_graph[key]:
                total += self.undirected_graph[key][word]

            if key == '$$':
                print(total)
            if out_frequencies.get(key, None) is not None:
                total -= next(iter(out_frequencies[key]))
            if key == '$$':
                print(total)
            in_frequencies[key] = {total: total / (self.totalEdges - numEdges)}

        self.__write_to_JSON(in_frequencies, indegree)

    def undirected_vertex_distribution(self, fname,
                                       outName="undirected_histogram.json"):
        """Calculates and outputs undirected graph vertex distribution

        Arguments:
            fname {str} -- Input file containing graph

        Keyword Arguments:
            outName {str} -- Output file
            (default: {"undirected_histogram.json"})
        """
        with open(fname, "r") as inFile:
            self.undirected_graph = json.load(inFile)

        self.totalEdges = self.__count_edges(self.undirected_graph,
                                             directed=False)
        frequencies = self.__calculate_frequency(self.undirected_graph,
                                                 self.totalEdges)
        self.__write_to_JSON(frequencies, outName)


def _check_usage(args):
    """Checks usage of program

    Arguments:
        args {list} -- List of command line arguments
    """
    if len(args) != 3:
        sys.exit("Usage: python degrees.py <file> <file>")


def main():
    _check_usage(sys.argv)

    degree = Degree()
    degree.undirected_vertex_distribution(sys.argv[1])
    degree.directed_vertex_distribution(sys.argv[2])


if __name__ == '__main__':
    main()
