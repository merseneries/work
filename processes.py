import csv
import datetime
import os
import time

import psutil


class Monitor:
    data = list()

    def __init__(self, process_name, process_pid=-1):
        self.name = process_name
        self.pid = process_pid

    def __get_path(self, file_name):
        """
        :param file_name: name of file with type
        """
        return os.getcwd() + os.sep + 'resources' + os.sep + file_name

    def __get_date(self):
        return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def csv_write(self, data, mode="w"):
        file_name = self.name.rsplit(".", 1)[0] + ".csv"
        file_path = self.__get_path(file_name)
        mode = "a" if mode != "w" else "w"
        with open(file_path, mode=mode, newline="") as file:
            header = ["Data", "Process_name", "Process_pid", "Cpu_percent", "Cpu_times_user",
                      "Cpu_times_system", "Memory_percent", "Memory_rss", "Memory_vms"]
            write_file = csv.writer(file, delimiter=";")
            if mode == "w":
                write_file.writerow(header)
            write_file.writerows(data)

    def get_process_stat(self, min_steps=5, timer_subprocess=1):

        """
        :param min_steps: how much scan for process
        :param timer_subprocess: how much seconds for 1 subprocess
        :return: list of data
        """

        result = []
        for times in range(min_steps):
            for process in psutil.process_iter():
                check_condition = process.name() == self.name if self.pid == -1 else process.pid == self.pid
                with process.oneshot():
                    if check_condition:
                        for i in range(timer_subprocess):
                            temp = [
                                self.__get_date(),
                                process.name(),
                                process.pid,
                                process.cpu_percent(),
                                process.cpu_times().user,
                                process.cpu_times().system,
                                process.memory_percent(),
                                process.memory_info().rss / (1024 * 1024),
                                process.memory_info().vms / (1024 * 1024)
                            ]
                        temp = list(
                            map(lambda x: " " + str(round(x, 2)) if type(x) == float else str(x), temp))
                        result.append(temp)
                        time.sleep(1.0)
            time.sleep(1.0)
        return result

    def get_now(self, timer_subprocess=1, delay=0):

        for process in psutil.process_iter():
            check_condition = process.name() == self.name if self.pid == -1 else process.pid == self.pid
            with process.oneshot():
                if check_condition:
                    temp = [
                        self.__get_date(),
                        process.name(),
                        process.pid,
                        process.cpu_percent(),
                        process.cpu_times().user,
                        process.cpu_times().system,
                        process.memory_percent(),
                        process.memory_info().rss / (1024 * 1024),
                        process.memory_info().vms / (1024 * 1024)
                    ]
                    temp = list(map(lambda x: " " + str(round(x, 2)) if type(x) == float else " " + str(x), temp))
                    self.data.append(temp)
                    time.sleep(delay)

