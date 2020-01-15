import datetime
import time
import unittest
import pyautogui as autogui
import pytesseract
import pyttsx3
import pytz
import selenium
import wolframalpha
from appium import webdriver
from monitor import Monitor
from my_funcs import Volume, Process

BROWSER = "Open microsoft.com"
PATH_CORTANA = r"C:\Windows\SystemApps\Microsoft.Windows.Cortana_cw5n1h2txyewy\SearchUI.exe"
PATH_WINDRIVER = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
PATH_ALARM = r"E:\PycharmProjects\TestBad\resources\Alarm.lnk"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Test_Cortana(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_caps = {}
        autogui.hotkey("win", "c")
        desired_caps["app"] = PATH_CORTANA
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
        autogui.press("esc")
        self.monitor = Monitor("SearchUI.exe")

    # @classmethod
    # def tearDownClass(self):
    #     self.driver.quit()

    def setUp(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 110)
        self.open_cortana()

    def tearDown(self):
        autogui.sleep(3)
        autogui.press("esc")
        print("Closed...")

    def open_cortana(self, voice=True):
        """
        Open Cortana with voice or hotkey
        :param voice: if true say "Hey Cortana" else with hotkeys
        """
        if voice:
            self.engine.say("Hey Cortana")
        else:
            autogui.hotkey("win", "c")
        print("Opening...")

    def say(self, text, timer=2):
        self.engine.say(text)
        self.engine.runAndWait()
        time.sleep(timer)

    def wait_listen(self):
        count = 0
        text_displayed = False
        while count < 10:
            try:
                text_displayed = self.driver.find_element_by_name("Listening... ").is_displayed()
                if text_displayed:
                    break
            except:
                time.sleep(1)
                count += 1

    @staticmethod
    def get_screenshot_text(area=(0, 0, 0, 0)):
        scr = autogui.screenshot(region=area)
        scr = scr.convert("L")
        first_pixel = scr.getpixel((0, 0))
        if first_pixel != 0 and first_pixel != 255:
            scr = scr.point(lambda x: 0 if x > 200 else 255)
        scr.save("image.png")
        return pytesseract.image_to_string(scr)

    @staticmethod
    def get_woflramalpha_result(request_text):
        client = wolframalpha.Client("TPLGT3-ETLWX6G6X3")
        res = client.query(request_text)
        return next(res.results).text

    @staticmethod
    def check_response(actual, expected):
        actual = actual.lower().replace(".", "").replace(",", "").split()
        expected = expected.lower().replace(".", "").replace(",", "").split()
        return any(i for i in actual if i in expected)

    def is_exist(self, name):
        try:
            self.driver.find_element_by_name(name)
        except selenium.common.exceptions.NoSuchWindowException:
            return False
        return True

    def monitor(iter=1):
        def time_recorder(func):
            def wrapper(self):
                for i in range(iter):
                    if i != 0:
                        self.setUp()

                    self.monitor.begin()
                    start = time.time()
                    func(self)
                    end = time.time()
                    self.monitor.end()

                    print("---------------------------")
                    print("Test #{0}\nTime spend: {1}".format(i, end - start))
                    print("---------------------------")

                    if i != iter - 1:
                        self.tearDown()

            return wrapper

        return time_recorder

    """
    
    ###------------------Functionality tests------------------###
    
    """

    def test_question(self):
        text_question = "Who is the first President of USA?"
        self.say(text_question)

        # check if response about President
        cortana_response = self.driver.find_element_by_accessibility_id("GreetingLine1").text
        self.assertTrue(self.check_response(text_question, cortana_response),
                        "Search not correct. Actual: '{}'. Expected: '{}'".format(text_question, cortana_response))

        # check if result correct President
        cortana_result = self.get_screenshot_text(area=(178, 600, 200, 40))
        woflram_result = self.get_woflramalpha_result(text_question).split(" (", 1)[0]
        self.assertIn(cortana_result, woflram_result, "Result not correct")

    def test_weather(self):
        text_city = "weather in Vinnytsya"
        self.say(text_city)

        # check if response about weather
        cortana_response = self.get_screenshot_text(area=(50, 471, 340, 30))
        self.assertTrue(self.check_response(text_city, cortana_response), "Search not about weather")

        # check if correct city selected
        cortana_result = self.get_screenshot_text(area=(50, 525, 160, 31))
        self.assertTrue(self.check_response(text_city, cortana_result), "Incorrect city")

    def test_calculator(self):
        text_math = "2 multiply by 18 equal"
        math_actual = 2 * 18
        self.say(text_math)

        # check if response about calculation
        cortana_response = self.driver.find_element_by_class_name("WebView").text
        # self.assertIn(text_math, cortana_response, "Text '{0}' not in Cortana response".format(text_math))
        self.assertTrue(self.check_response(text_math, cortana_response), "Search not about calculator")

        # check if correct calculation
        cortana_result = self.driver.find_element_by_accessibility_id("rcHead").text
        self.assertEqual(str(math_actual), cortana_result, "{0} don't equal {1}".format(math_actual, cortana_result))

    # def test_open_calendar(self):
    #     text_open = "calendar"
    #     self.say(text_open)
    #
    #     # check if response about calendar
    #     # cortana_response = self.driver.find_element_by_class_name("WebView").text
    #     cortana_response = self.get_screenshot_text(area=(50, 500, 325, 60))
    #     self.assertTrue(self.check_response(text_open, cortana_response), "Search not about calendar")
    #     # self.assertIn(text_open, cortana_response,"Trying to open '{0}' but response is '{1}'".format(text_open, cortana_response))
    #     self.wait_listen()
    #     self.say(text_open)
    #
    #     # check if correct program opened
    #     cortana_result = self.get_screenshot_text(area=(60, 505, 325, 40))
    #     self.assertTrue(self.check_response(text_open, cortana_result), "Must opened calendar")
    #
    # def test_convert(self):
    #     text_convert = "How much seconds in week"
    #     actual_convert = 7 * 24 * 60 * 60
    #     self.say(text_convert)
    #
    #     # check if response about convert
    #     cortana_response = self.get_screenshot_text(area=(55, 532, 100, 25))
    #     self.assertTrue(self.check_response(text_convert, cortana_response), "Search not about convert")
    #
    #     # check if correct convert result
    #     cortana_result = self.get_screenshot_text(area=(55, 561, 121, 30))
    #     self.assertTrue(self.check_response(str(actual_convert), cortana_result))
    #
    # def test_volume(self):
    #     volume = Volume()
    #     start_level = volume.get_level()
    #
    #     text_volume = "Decrease volume by 30"
    #     self.say(text_volume)
    #     changed_level = volume.get_level()
    #
    #     print("Start", start_level, "Changed", changed_level)
    #     self.assertNotEqual(start_level, changed_level, "Volume didn't change")
    #
    #     volume.set_volume(100)
    #
    # def test_open_excel(self):
    #     excel_process = "EXCEL.EXE"
    #
    #     text_open = "Open excel"
    #     self.say(text_open)
    #
    #     # check if response about excel
    #     cortana_response = self.get_screenshot_text(area=(50, 490, 150, 50))
    #     self.assertTrue(self.check_response(text_open, cortana_response), "Search not about excel")
    #
    #     time.sleep(5)
    #     # check if excel opened
    #     self.assertTrue(Process.is_alive(excel_process), "Excel didn't open")
    #
    #     Process.kill(excel_process)
    #
    # def test_alarm(self):
    #     text_alarm = "Set alarm tomorrow at 11 am"
    #     self.say(text_alarm, 6)
    #
    #     # check if response about set alarm
    #     cortana_response = self.get_screenshot_text(area=(55, 560, 150, 55))
    #     self.assertTrue(self.check_response(text_alarm, cortana_response), "Search not about alarm")
    #
    #     Process.open(PATH_ALARM)
    #     # add check if system set alarm in app
    #
    #     self.open_cortana()
    #     self.say("Delete all alarms")
    #
    # def test_time(self):
    #     text_time = "What time in Tokyo?"
    #     self.say(text_time)
    #
    #     # check if response about time
    #     cortana_response = self.driver.find_element_by_accessibility_id("GreetingLine1").text
    #     self.assertTrue(self.check_response(text_time, cortana_response), "Search not about time")
    #
    #     cortana_result = self.get_screenshot_text(area=(150, 560, 200, 80)).replace("\n\n", " ")
    #     actual_tokyo = datetime.datetime.now(pytz.timezone("Asia/Tokyo")) \
    #         .strftime(" %I:%M %p %a, %b %d, %Y").replace(" 0", "")
    #     self.assertEqual(actual_tokyo, cortana_result, "Result doesn't equal")
    #
    # def test_image(self):
    #     text_image = "Show images of dogs"
    #     self.say(text_image)
    #
    #     # check if response about image
    #     cortana_response = self.driver.find_element_by_accessibility_id("GreetingLine1").text
    #     self.assertTrue(self.check_response(text_image, cortana_response), "Search not about images")

    # def test_route(self):
    #     text_route = "Show me route from London to Berlin"
    #     self.say(text_route)

    # def test_translate(self):
    #     text_translate = "Translate extraordinary human to ukrainian"
    #     self.say(text_translate)
    #
    #     # check if correct response
    #     # cortana_result = self.get_screenshot_text(area=(60, 710, 200, 45))
    #     # self.assertEqual("надзвичайна людина", cortana_result, "Translate incorrect")

    # def test_video(self):
    #     text_time = "Play video in YouTube about Iron man"
    #     self.say(text_time)

    # def test_music(self):
    #     text_music = "Open Groove music"
    #     self.say(text_music, 8)
    #     autogui.press("volumedown", presses=4)
    #     autogui.press("enter")
    #
    # def test_movie(self):
    #     test_movie = "Open Movies & TV"
    #     self.say(test_movie, 8)
    #
    #     autogui.press("enter")
    #     autogui.sleep(1)
    #     autogui.press("enter")
    #
    # def test_email(self):
    #     text_email = "Send email to Jared about What you will do tomorrow?"
    #     self.say(text_email)

    """
    
    ###------------------Smoke tests------------------###
    
    """

    # def test_smoke_1(self):
    #     text_expected = "Cortana"
    #     cortana_response = self.driver.find_element_by_name(text_expected).text
    #     self.assertEqual(text_expected, cortana_response, "Cortana doesn't open")

    # def test_smoke_2(self):
    #     self.say("What time is it?")
    #
    #     cortana_response = self.get_screenshot_text(area=(150, 560, 200, 50))
    #     current_time = time.strftime(" %I:%M %p").lstrip(" 0").replace("0", "")
    #     self.assertEqual(current_time, cortana_response, "Time doesn't equal")

    # def test_smoke_3(self):
    #     text_open = "Open settings"
    #     self.say(text_open)
    #
    #     cortana_response = self.get_screenshot_text(area=(50, 450, 325, 60))
    #     self.assertTrue(self.check_response(text_open, cortana_response), "Setting didn't open")

    # def test_smoke_4(self):
    #     self.say("", 15)
    #     check_exist = self.is_exist("Cortana")
    #     self.assertFalse(check_exist, "Cortana didn't close after say nothing")

    # def test_smoke_5(self):
    #     self.say("Грай музику", 15)
    #     check_exist = self.is_exist("Cortana")
    #     self.assertFalse(check_exist, "Cortana didn't close")

    """

    ###------------------Performance tests------------------###

    """

    # @monitor(iter=4)
    # def test_performance_1(self):
    #     self.say("What time is it?", 5)
    #


if __name__ == '__main__':
    unittest.main()
