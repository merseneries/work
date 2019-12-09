import csv
import os
import requests


def get_path(file_name):
    """
    :param file_name: name of file with type
    """
    return os.getcwd() + os.sep + 'resources' + os.sep + file_name


FILE_NAME = "book.csv"
FILE_NAME_2 = "book.csv_2"


def file_read(name_file):
    full_path = get_path(name_file)

    with open(full_path, "r") as file:
        read_csv = csv.DictReader(file, delimiter=";")
        result = []
        for row in read_csv:
            response = requests.get(row.get("URL"))
            time_response = response.elapsed.total_seconds() if response.status_code == 200 else "Null"
            # time_response = response.elapsed.total_seconds()
            result.append({"URL": row.get("URL"), "Time": time_response})
    return result


def file_write(name_file, data):
    full_path = get_path(name_file)
    with open(full_path, "w", newline='\n') as file:
        write_csv = csv.DictWriter(file, fieldnames=["URL", "Time"], delimiter=";")
        write_csv.writeheader()
        write_csv.writerows(data)


data_file = file_read(FILE_NAME)
file_write(FILE_NAME, data_file)
