import datetime

import psutil
from pandas import DataFrame

from my_funcs import get_path

CURRENT_DATE = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
NAME = "pycharm64.exe"
NAME_FILE = "test.csv"


def csv_write(name_file, data):
    cars = [['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
            [22000, 25000, 27000, 35000]]
    df = DataFrame(cars)
    df.to_csv(get_path(NAME_FILE), sep=";")


def process_statistics(process_name):
    result = []
    for process in psutil.process_iter():
        with process.oneshot():
            if process.name() == process_name:
                # result.append({Date:})
                print(process.name(), process.memory_info(), sep="  \n")
                break
    # for process in psutil.process_iter():
    # if process.name() == "chrome.exe":
    #     print(process)

# process_statistics(NAME)
