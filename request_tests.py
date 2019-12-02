import requests

URL = "https://api.weather.com/v2/turbo/vt1observation?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode=49.23%2C28.47&language=uk-UA&units=m"
PARAMS = {}
response = requests.get(URL)
data_response = response.json()
weather_params = data_response["vt1observation"]
# result = [key + " " + str(item) for key, item in weather_params.items()]
result_2 = ["Температува:" + str(weather_params["temperature"]), weather_params["phrase"],
            "За відчуттям:" + str(weather_params["feelsLike"])]

for e in result_2:
    print(e)
