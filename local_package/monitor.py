import datetime
import psutil
import time
import os
import csv
from multiprocessing import Process, freeze_support
from local_package.funcs import get_resource


class Monitor:

    def __init__(self, process_name):
        self.name = process_name
        self.process = 0

    def get_path(self, file_name):
        """
        :param file_name: name of file with type
        """
        return os.getcwd() + os.sep + 'resources' + os.sep + file_name

    def csv_write(self, data):
        file_name = self.name.rsplit(".", 1)[0] + ".csv"
        file_path = get_resource("", file_name)
        # mode = "a" if mode != "w" else "w"
        # field_names = ["Date", "Process_name", "Cpu_percent", "Memory_percent", "Memory_rss", "Memory_vms"],
        with open(file_path, "a", newline='\n') as file:
            write_csv = csv.writer(file, delimiter=";")
            write_csv.writerow(data)

    def get_date(self):
        return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def scan(self):
        while True:
            for process in psutil.process_iter():
                if process.name() == self.name:
                    with process.oneshot():
                        temp = [
                            self.get_date(),
                            process.name(),
                            process.cpu_percent(),
                            # process.cpu_times().user,
                            # process.cpu_times().system,
                            process.memory_percent(),
                            process.memory_info().rss / (1024 * 1024),
                            process.memory_info().vms / (1024 * 1024)
                        ]
                        temp = list(map(lambda x: " " + str(round(x, 2)) if type(x) == float else " " + str(x), temp))
            time.sleep(1)
            self.csv_write(temp)

    def begin(self):
        self.process = Process(target=self.scan)
        self.process.start()

    def end(self):
        self.process.terminate()


if __name__ == '__main__':
    freeze_support()
