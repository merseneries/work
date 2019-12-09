import requests
import datetime

CURRENT_DATE = datetime.datetime.now().strftime("%d.%m.%Y")
URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="


def cuex():
    URL = "https://api.cuex.com/v1/exchanges/usd?to_currency=uah&from_date="
    param = {}
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    response = requests.get(URL + current_date)
    data_json = response.json()
    selected_data = data_json["data"][0]["rate"]
    print("Money rate 1$ to UAH on:", current_date, "is", str(selected_data)[:5])


def get_rate(date, url):
    response = requests.get(url + date)
    data_json = response.json()
    selected_data = data_json["exchangeRate"]
    # result = [line["saleRateNB"] for line in selected_data if line.get("currency") == "USD"]
    for line in selected_data:
        if line.get("currency") == "USD":
            return line["saleRateNB"]


usd_rate = get_rate(CURRENT_DATE, URL)

input_result = int(input("Press 1 or 2:\n 1.UAH to USD\n 2.USD to UAH\n"))
if input_result == 1 or input_result == 2:
    input_sum = float(input("What sum: "))
    result = input_sum / usd_rate if input_result == 1 else usd_rate * input_sum
    print("{0:.2f}".format(result))
else:
    print("Wrong input")
