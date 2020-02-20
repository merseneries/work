import time
import random

two_dimensional = [
    [12, 45, 1, 0, 66],
    [47, 32, 11, 7, 17],
    [65, 90, 21, 3, 16],
    [0, -16, 22, 12, 33]
]

one_dim = [random.randint(-100, 100) for i in range(100)]


def timer(func):
    def wrapper(arg):
        start = time.time_ns()
        arr = func(arg)
        end = time.time_ns()
        print(f"Run time: {end - start} ns")
        return arr

    return wrapper


def list_no_duplicates(array):
    one_dimensional = []
    for i in array:
        one_dimensional += i
    return bubble_sort(one_dimensional), len(one_dimensional)


@timer
def bubble_sort(array):
    arr_len = len(array)

    if arr_len == 0:
        return 0

    for j in range(arr_len):
        for i in range(arr_len - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
    return array


def count_sort(array):
    """
        One loop that count frequency of numbers. Only for +int?
    """
    pass


result_no_ordered, list_length = list_no_duplicates(two_dimensional)
print("List length: {} \nList: {}\nSorted: {} \nLength after: {}"
      .format(list_length, two_dimensional, result_no_ordered, len(result_no_ordered)))
