import os


def get_path(file_name):
    """
    Get current path and add file name in that with type
    :param file_name: name of file with type
    """
    return os.getcwd() + os.sep + file_name


def get_resource(dir_name, file_name):
    """
    Get path to directory resources
    :param dir_name: name of the directory, create if not exist
    :param file_name: name of the file
    :return: full path with directory and file name
    """

    dir_resources = r"E:\PycharmProjects\TestBad\resources"
    file_path = dir_resources + os.sep + dir_name
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path + os.sep + file_name


def list_min(array, min_values=2):
    arr_len = len(array)
    for j in range(arr_len):
        for i in range(arr_len - 1):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
    return array[:min_values]
