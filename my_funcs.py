import os


def get_path(file_name):
    """
    :param file_name: name of file with type
    """
    return os.getcwd() + os.sep + 'resources' + os.sep + file_name
