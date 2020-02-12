import sys
import matplotlib.pyplot as plt
from local_package.funcs import *

FILE_NAME = "Emissions.csv"
OUTPUT_FILE = "User_selection"


def get_file_data(file_name):
    file_path = get_path(FILE_NAME)
    file_data = csv_read(file_path)

    data_dict = {}
    for line in file_data:
        data_dict[line[0]] = [float(i) if "." in i else i for i in line[1:]]
    return data_dict


def get_stats(data, year):
    max = (-sys.maxsize, 0)
    min = (sys.maxsize, 0)
    avg = []
    list_all_data = list(data.values())
    list_keys = list(data.keys())
    list_years = list_all_data[0]

    try:
        cell = list_years.index(year)
        for i, v in enumerate(list_all_data[1:], 1):
            tmp = float(v[cell])
            if tmp > max[0]:
                max = tmp, list_keys[i]
            elif tmp < min[0]:
                min = tmp, list_keys[i]
            avg.append(tmp)
        avg = sum(avg) / len(avg)
    except ValueError:
        print("Error: year", year, "not in list")
        return

    return {"min": min, "max": max, "avg": avg}


def plot_data(*country, data):
    plt.subplot()
    for i in country:
        key_index = list(data.keys()).index(i)
        y_data = list(data.values())[key_index]
        x_data = list(data.values())[0]
        plt.plot(x_data, y_data, label=i)
    plt.legend()
    plt.xlabel("Years")
    plt.ylabel("Emissions")
    plt.grid(True)
    plt.show()


def get_selected(*country, data):
    data = data.copy()
    keys_data = list(data.keys())
    temp = [[keys_data[0]] + list(data.values())[0]]

    for c in country:
        for i, v in enumerate(keys_data[1:]):
            if c == v:
                temp.append([c]+data[c])
    return temp


data_dict = get_file_data(FILE_NAME)
select_data = get_selected("Ukraine", "Austria", "Singapore", data=data_dict)
csv_write(OUTPUT_FILE, select_data)
stats_dict = get_stats(data_dict, "2002")
plot_data("Ukraine", "Austria", "Singapore", data=data_dict)

"""
    This only for other branch.
    Push only there.
"""
