import requests
import datetime

URL = "https://api.weather.com/v2/turbo/vt1observation?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=49.23%2C28.47&language=uk-UA&units=m"
response = requests.get(URL)
data_response = response.json()
weather_params = data_response["vt1observation"]
# result = [key + " " + str(item) for key, item in weather_params.items()]
result_2 = ["Температува:" + str(weather_params["temperature"]), weather_params["phrase"],
            "За відчуттям:" + str(weather_params["feelsLike"])]

# for e in result_2:
#     print(e)

URL = "https://api.cuex.com/v1/exchanges/usd?to_currency=uah&from_date="
param = {}
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
response = requests.get(URL + current_date)
data_json = response.json()
selected_data = data_json["data"][0]["rate"]
print("Money rate 1$ to UAH on:", current_date, "is", str(selected_data)[:5])

