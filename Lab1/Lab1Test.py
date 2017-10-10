import matrix_multiplier
from sys import argv
from random import randrange
from time import time
import csv
import numpy as np


def main():
    if len(argv) != 2:
        print("Usage: Lab1Test.py <file>")
        return

    matrixMultiplier = matrix_multiplier.MatrixMultiplier()
    with open(argv[1]) as file:
        sizeList = file.readline().strip().split(" ")
        repetitions = int(file.readline())

    with open("test.csv", "w") as output:
        csvWriter = csv.writer(output)
        csvWriter.writerow(['Size',
                           'Iterative', 'Iterative Standard Deviation',
                           'Recursive', 'Recursive Standard Deviation',
                           'Strassens', 'Strassens Standard Deviation'])

        for size in sizeList:
            iterative_time = []
            recursive_time = []
            strassens_time = []
            for i in range(repetitions):
                A = [[randrange(100) for j in range(int(size))]
                     for k in range(int(size))]
                B = [[randrange(100) for j in range(int(size))]
                     for k in range(int(size))]

                n = m = k = len(A)

                start = time()
                matrixMultiplier.iterative_multiplication(n, k, m, A, B)
                end = time()
                iterative_time.append(end - start)

                start = time()
                matrixMultiplier.MMDC(n, np.array(A), np.array(B))
                end = time()
                recursive_time.append(end - start)

                start = time()
                matrixMultiplier.strassens_algorithm(n, k, m, A, B)
                end = time()
                strassens_time.append(end - start)

            iterative_average_time = np.mean(np.array(iterative_time))
            recursive_average_time = np.mean(np.array(recursive_time))
            strassens_average_time = np.mean(np.array(strassens_time))

            iterative_deviation = np.std(np.array(iterative_time))
            recursive_deviation = np.std(np.array(recursive_time))
            strassens_deviation = np.std(np.array(strassens_time))
            
            csvWriter.writerow([size,
                               iterative_average_time, iterative_deviation,
                               recursive_average_time, recursive_deviation,
                               strassens_average_time, strassens_deviation])


if __name__ == '__main__':
    main()
