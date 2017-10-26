import json
import sys


class Connected():
    """Outputs graph connectedness information"""
    def __init__(self, barrier="*" * 10):
        """Sets the barrier when writing

        Sets the barrier when writing the txt file.

        Keyword Arguments:
            barrier {str} -- The barrier in the txt file (default: {"*" * 10})
        """
        self.barrier = barrier

    def show_connectedness(self, fname, outName="connected.txt"):
        """Shows the connectedness of the graph in fname

        Opens the file associated with fname and outputs information about
        the connectedness of the graph inside.
        This file contains an undirected weighted graph in JSON format.

        Arguments:
            fname {str} -- The file containing the graph
            outName {str} -- The name of the outFile
            (default: {"connected.txt"})
        """
        with open(fname, "r") as inFile:
            graph = json.load(inFile)

        with open(outName, "w") as outFile:
            outFile.write("%s\nTotal number of connected components: %s\n"
                          % (self.barrier, len(graph)))

            outFile.write("%s\nWord | # Components | Max Degree :" %
                          self.barrier + "# Vertices w/ Max Degree | " +
                          "Word List w/ Max Degree\n")
            outFile.write("-" * 76 + "\n")
            for key in sorted(graph):
                numComponents = len(graph[key])
                sortedDegrees = sorted(graph[key].values(), reverse=True)
                maxDegree = sortedDegrees[0]
                numMaxDegree = sortedDegrees.count(maxDegree)
                maxDegreeList = [word for word in sorted(graph[key])
                                 if graph[key][word] == maxDegree]
                if numMaxDegree > 20:
                    maxDegreeList[:20]
                outFile.write("\n%-28s | %4d | %4d : %-4d | " %
                              (key, numComponents, maxDegree, numMaxDegree))
                outFile.write("%s " % maxDegreeList)


def _check_usage(args):
    """Checks usage of program

    Arguments:
        args {list} -- List of command line arguments
    """
    if len(args) != 2:
        sys.exit("Usage: python connected.py <file>")


def main():
    _check_usage(sys.argv)

    connected = Connected()
    connected.show_connectedness(sys.argv[1])


if __name__ == '__main__':
    main()
