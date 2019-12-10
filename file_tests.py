import csv

import requests

from my_funcs import get_path

FILE_NAME = "book.csv"


def func_decorator(func):
    import time

    def wrapped(*args):
        start = time.time()
        return_value = func(*args)
        end = time.time()
        time_response = return_value.elapsed.total_seconds() if return_value.status_code == 200 else "Null"
        return time_response, end - start

    return wrapped


@func_decorator
def get_response(url):
    return requests.get(url)


def file_read(name_file):
    full_path = get_path(name_file)

    with open(full_path, "r") as file:
        read_csv = csv.DictReader(file, delimiter=";")
        result = []
        for row in read_csv:
            time_response, time_sys = get_response(row.get("URL"))
            # time_response = response.elapsed.total_seconds() if response.status_code == 200 else "Null"
            result.append({"URL": row.get("URL"), "Time": time_response, "Time_sys": round(time_sys, 6)})
    return result


def file_write(name_file, data):
    full_path = get_path(name_file)
    with open(full_path, "w", newline='\n') as file:
        write_csv = csv.DictWriter(file, fieldnames=["URL", "Time", "Time_sys"], delimiter=";")
        write_csv.writeheader()
        write_csv.writerows(data)


data_file = file_read(FILE_NAME)
file_write(FILE_NAME, data_file)
