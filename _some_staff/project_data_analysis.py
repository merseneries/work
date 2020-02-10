import sys
import matplotlib.pyplot as plt
from local_package.funcs import *

FILE_NAME = "Emissions.csv"


def get_data(file_name):
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
        print("Year", year, "not in list")

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


data_dict = get_data(FILE_NAME)
stats_dict = get_stats(data_dict, "2002")
plot_data("Ukraine", "Austria", "Singapore", data=data_dict)
