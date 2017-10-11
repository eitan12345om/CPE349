import csv
import median
import numpy as np
from random import randrange
from sys import argv
from time import time


def main():
    if len(argv) != 2:
        print("Usage: Lab2Test.py <file>")
        return

    median_obj = median.Median()
    with open(argv[1], "r") as file:
        sizeList = file.readline().strip().split(" ")
        repetitions = int(file.readline())

    with open("test.csv", "w") as output:
        csvWriter = csv.writer(output)
        csvWriter.writerow(['Size',
                            'Sort-Based', 'Sort-Based Std Dev',
                            'Randomized Median', 'Randomized Median Std Dev',
                            'Fast Median (k=3)', 'Fast Median (k=3) Std Dev',
                            'Fast Median (k=5)', 'Fast Median (k=5) Std Dev',
                            'Fast Median (k=7)', 'Fast Median (k=7) Std Dev'])

        for size in sizeList:
            sort_based_time = []
            randomized_time = []
            fast3_time = []
            fast5_time = []
            fast7_time = []
            for i in range(repetitions):
                A = [[randrange(100) for j in range(int(size))]
                     for k in range(int(size))]

                start = time()
                # Is this right?
                median_obj.get_median(A)
                end = time()
                sort_based_time.append(end - start)

                start = time()
                # Is this right?
                median_obj.randomized_median(A, len(A) % 2 == 0)
                end = time()
                randomized_time.append(end - start)

                start = time()
                median_obj.fast_median(A, 3)
                end = time()
                fast3_time.append(end - start)

                start = time()
                median_obj.fast_median(A, 5)
                end = time()
                fast5_time.append(end - start)

                start = time()
                median_obj.fast_median(A, 7)
                end = time()
                fast7_time.append(end - start)

            sort_based_average_time = np.mean(np.array(sort_based_time))
            randomized_average_time = np.mean(np.array(randomized_time))
            fast3_average_time = np.mean(np.array(fast3_time))
            fast5_average_time = np.mean(np.array(fast5_time))
            fast7_average_time = np.mean(np.array(fast7_time))

            sort_based_deviation = np.std(np.array(sort_based_time))
            randomized_deviation = np.std(np.array(randomized_time))
            fast3_deviation = np.std(np.array(fast3_time))
            fast5_deviation = np.std(np.array(fast5_time))
            fast7_deviation = np.std(np.array(fast7_time))

            csvWriter.writerow([size,
                               sort_based_average_time, sort_based_deviation,
                               randomized_average_time, randomized_deviation,
                               fast3_average_time, fast3_deviation,
                               fast5_average_time, fast5_deviation,
                               fast7_average_time, fast7_deviation])


if __name__ == "__main__":
    main()
