import random
import math


class Median:
    def __init__(self):
        """
        Initializes a Median object
        """
        pass

    def get_median(self, data):
        l = len(data) - 1
        if len(data) % 2 != 0:
            return data[int(l/2)]
        return (data[int(l/2)] + data[int((l/2) + 1)])/2

    """
        part 2
    """
    def randomized_median(self, data, even=False):
        n_index = len(data) - 1
        middle_index_1 = int((len(data) + 1) / 2)  # odd size array
        middle_index_2 = math.ceil((len(data) + 1) / 2)

        if even:
            median_num_1 = self.quick_select(data, 0, n_index, middle_index_1)
            median_num_2 = self.quick_select(data, 0, n_index, middle_index_2)
            median = (median_num_1 + median_num_2)/2
        else:
            median = self.quick_select(data, 0, n_index, middle_index_1)
        print("Median number: ", median)

    def partition(self, data, l, r):
        pivot_num = data[r]
        i = l - 1
        j = l
        while j <= r - 1:
            if data[j] <= pivot_num:
                i = i + 1
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
            j += 1
        temp = data[i+1]
        data[i+1] = data[r]
        data[r] = temp
        new_pivot_point = i + 1
        return new_pivot_point

    def randomize_partition(self, data, l, r):
        pivot = random.randint(l, r)
        temp = data[pivot]
        data[pivot] = data[r]
        data[r] = temp
        return self.partition(data, l, r)

    def quick_select(self, data, l, r, i):
        if l == r:
            return data[l]
        pivot = self.randomize_partition(data, l, r)

        k = pivot - l + 1
        if i == k:
            return data[pivot]
        elif i < k:
            return self.quick_select(data, l, pivot - 1, i)
        else:
            return self.quick_select(data, pivot + 1, r, i - k)

    """
        part 1
    """
    def sort_based(self, data):
        n = len(data) - 1
        self.merge_sort(data, 0, n)
        self.get_median(data)

    def merge(self, data, l, m, r):
        temp_size_1 = m - l + 1
        temp_size_2 = r-m

        L = [0] * temp_size_1
        R = [0] * temp_size_2

        for i in range(0, temp_size_1):
            L[i] = data[l + i]
        for j in range(0, temp_size_2):
            R[j] = data[m + 1 + j]

        i = 0
        j = 0
        k = l

        while i < temp_size_1 and j < temp_size_2:
            if L[i] <= R[j]:
                data[k] = L[i]
                i = i + 1
            else:
                data[k] = R[j]
                j = j + 1
            k = k + 1

        while i < temp_size_1:
            data[k] = L[i]
            i = i + 1
            k = k + 1

        while j < temp_size_2:
            data[k] = R[j]
            j = j + 1
            k = k + 1

    def merge_sort(self, data, l, r):
        if l < r:
            m = int((l + (r - 1)) / 2)
            self.merge_sort(data, l, m)
            self.merge_sort(data, m + 1, r)
            self.merge(data, l, m, r)

    """
        part 3
    """
    def fast_median(self, array, k=5):
        """Determines the median of an array

        Finds the median of an array by splitting up into n/k chunks.
        The median of each chunk is found and the median of medians is found.

        It is unknown what the best value for k is. This class
        expects the usage of k as 3, 5, and 7.
        Both 5 and 7 are very efficient and better than 3.

        Arguments:
            array {[1...N]} -- Array for which to find the median
            k {int} -- The number of elements per chunk (default: 5)
        """
        if (len(array) <= k):
            # TODO: Sort and return median
            pass

        median_of_subsets = []
        for i in range(0, len(array), k):
            median_of_subsets.append(self.fast_median(array[i: i + k], k))

        # TODO: Sort and return median
        return
