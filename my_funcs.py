import os


# some_list = [10, 20, 323, 0, -1, 2, 12, -40, 4, 11]
# rand_list = [random.randint(-100, 100) for i in range(10)]


def get_path(file_name):
    """
    :param file_name: name of file with type
    """
    return os.getcwd() + os.sep + 'resources' + os.sep + file_name


def list_min(array, min_values=2):
    arr_len = len(array)
    for j in range(arr_len):
        for i in range(arr_len - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
    return array[:min_values]
