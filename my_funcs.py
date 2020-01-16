import os
import subprocess
import re
import psutil


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


def kill_process(name):
    for process in psutil.process_iter():
        if process.name() == name:
            process.kill()


class Volume:
    PATH = r"E:\PycharmProjects\TestBad\resources\programs\SetVol.exe "
    REPORT = "report"

    def __init__(self):
        self.level = self.get_level()

    def get_level(self):
        result = subprocess.check_output(self.PATH + self.REPORT).decode("utf-8")
        current_volume = re.search(r"\d+", result)
        return current_volume.group()

    def set_volume(self, number):
        subprocess.call(self.PATH + str(number))

    def decrease(self, number):
        subprocess.call(self.PATH + "-" + str(number))

    def increase(self, number):
        subprocess.call(self.PATH + "+" + str(number))

    def mute(self):
        subprocess.call(self.PATH + "mute")

    def unmute(self):
        subprocess.call(self.PATH + "unmute")


class Process:
    @staticmethod
    def open(name):
        subprocess.call(name, shell=True)

    @staticmethod
    def is_alive(name):
        for process in psutil.process_iter():
            if process.name() == name:
                return True
        return False

    @staticmethod
    def kill(name):
        for process in psutil.process_iter():
            if process.name() == name:
                process.kill()
