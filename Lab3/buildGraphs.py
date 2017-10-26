import json
import sys


class GraphBuilder():
    """Builds a graph"""
    def __init__(self):
        pass

    def build_directed_graph(self, file):
        """Builds a directed weighted graph

        Takes in a csv file of wordgame results and converts the associations
        to a directed graph.

        Arguments:
            file {str} -- The file to open
        """
        graph = {}
        with open(file, "r") as inFile:
            inFile.readline()  # gets rid of header line

            for line in inFile:
                line = line.split(",")
                received = line[1]
                response = line[2]
                if len(received.split(" ")) == 1 and \
                   len(response.split(" ")) == 1:

                    # Make adjacency list
                    if received in graph:
                        if response in graph[received]:
                            graph[received][response] += 1
                        else:
                            graph[received].update({response: 1})
                    else:
                        graph[received] = {response: 1}

        self.__write_graph("directedGraph.json", graph)

    def build_undirected_graph(self, file):
        """Builds an undirected weighted graph

        Takes in a csv file of wordgame results and converts the associations
        to an undirected graph.

        Arguments:
            file {str} -- The file to open
        """
        graph = {}
        with open(file, "r") as inFile:
            inFile.readline()  # gets rid of header line

            for line in inFile:
                line = line.split(",")
                received = line[1]
                response = line[2]
                if len(received.split(" ")) == 1 and \
                   len(response.split(" ")) == 1:

                    # Make adjacency list
                    if received in graph:
                        if response in graph[received]:
                            graph[received][response] += 1
                        else:
                            graph[received].update({response: 1})
                    else:
                        graph[received] = {response: 1}

                    # Fix double numbers bug
                    if response != received:
                        if response in graph:
                            if received in graph[response]:
                                graph[response][received] += 1
                            else:
                                graph[response].update({received: 1})
                        else:
                            graph[response] = {received: 1}

        self.__write_graph("undirectedGraph.json", graph)

    def __write_graph(self, fname, graph):
        """Writes graph to JSON file

        Private method to write graphs into specified JSON file.
        Called by undirectedGraph and directedGraph.

        Arguments:
            fname {str} -- name of the file to write to
            graph {dictionary} -- adjacency list of words
        """
        with open(fname, "w") as outFile:
            json.dump(graph, outFile, indent=4, sort_keys=True)


def _check_usage(args):
    """Checks usage of program

    Arguments:
        args {list} -- List of command line arguments
    """
    if len(args) != 2:
        sys.exit("Usage: python buildGraphs.py <file>")


def main():
    _check_usage(sys.argv)

    graphBuilder = GraphBuilder()
    graphBuilder.build_directed_graph(sys.argv[1])
    graphBuilder.build_undirected_graph(sys.argv[1])


if __name__ == '__main__':
    main()
