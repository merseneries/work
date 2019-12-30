import pyttsx3
import requests
from gtts import gTTS
from playsound import playsound

text = """
The White House sought to freeze aid to Ukraine just 91 minutes after President Trump spoke to President Volodymyr 
Zelensky by phone in July, a newly-released government email has revealed.
"""


def text_speech(input_text):
    tts = gTTS(input_text)
    file_sound = "sound.mp3"
    tts.save(file_sound)
    playsound(file_sound)


def ttx3(input_text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # set female voice
    engine.setProperty('voice', voices[1].id)
    # set speaking rate
    engine.setProperty('rate', 150)
    engine.say(input_text)
    engine.runAndWait()
    # tts = gTTS(input_text)
    # tts.save(get_path("test.wav"))


def weather_request():
    CITY = "Vinnytsia,ua"
    KEYAPI = "79e2ef1a3de8fa7c5a8afb2d87ba778e"
    URL = "http://api.openweathermap.org/data/2.5/weather?"
    params = {"q": CITY, "units": "metric", "appid": KEYAPI}

    response = requests.get(URL, params)
    data_json = response.json()

    weather_param = ["weather", "main", "wind", "clouds", "name"]
    weather_data = [data_json[k] for k in weather_param]

    result = "Currently in " + weather_data[-1] + " "
    weather_main = [round(weather_data[1][k]) for k in ["temp", "feels_like", "humidity"]]
    result += "{0} degree. Feels like {1}. Humidity {2}%. ".format(*weather_main)
    result += "Wind speed " + str(round(weather_data[2]["speed"])) + " meters per second. Cloudiness " + str(
        weather_data[3]["all"]) + "%. "
    result += weather_data[0][0]["description"].capitalize()
    print(result)
    return result


weather_info = weather_request()
ttx3(weather_info)
