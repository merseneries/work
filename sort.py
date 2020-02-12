two_dimensional = [
    [12, 45, 1, 0, 66],
    [47, 32, 11, 7, 17],
    [65, 90, 21, 3, 16],
    [0, -16, 22, 12, 33]
]


def list_no_duplicates(array):
    one_dimensional = []
    for i in array:
        one_dimensional += i
    return sort_list(one_dimensional), len(one_dimensional)


def sort_list(array):
    tmp = 0
    arr_len = len(array)

    if arr_len == 0:
        return 0

    for j in range(arr_len):
        for i in range(arr_len - 1):
            if array[i] > array[i + 1]:
                tmp = array[i]
                array[i] = array[i + 1]
                array[i + 1] = tmp
    return array


result_no_ordered, list_length = list_no_duplicates(two_dimensional)
print("List length: {} \nList: {}\nSorted: {} \nLength after: {}"
      .format(list_length, two_dimensional, result_no_ordered, len(result_no_ordered)))