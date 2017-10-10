import median
import statistics
from sys import argv


def main():
    index = 0
    data = []
    if len(argv) != 2:
        print("Usage: Lab2Test.py <file>")
        return

    median_obj = median.Median()
    with open(argv[1], "r") as file:
        for line in file:
            for num in line.split():
                """
                when reading numbers in from a file convert them to integers!
                """
                data.append(int(num))
                index = index + 1

    median_obj.randomized_median(data, len(data) % 2 == 0)
    print("Compare Value: ", statistics.median(data))


if __name__ == "__main__":
    main()
