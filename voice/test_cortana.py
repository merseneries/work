import time
import unittest

import pyautogui as autogui
import pytesseract
import pyttsx3
import selenium
import wolframalpha
from appium import webdriver

BROWSER = "Open microsoft.com"
PATH_CORTANA = r"C:\Windows\SystemApps\Microsoft.Windows.Cortana_cw5n1h2txyewy\SearchUI.exe"
PATH_WINDRIVER = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class Test_Cortana(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_caps = {}
        autogui.hotkey("win", "c")
        desired_caps["app"] = PATH_CORTANA
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)
        autogui.press("esc")

    # @classmethod
    # def tearDownClass(self):
    #     self.driver.quit()

    def setUp(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 110)
        self.open_cortana()

    def tearDown(self):
        autogui.press("esc")
        print("Closed...")

    def open_cortana(self):
        self.engine.say("Hey Cortana")
        print("Opening...")
        # autogui.hotkey("win", "c")

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
        scr.save("image.jpeg")
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
                    start = time.time()
                    func(self)
                    end = time.time()
                    print("---------------------------")
                    print("Test #{0}\nTime spend: {1}".format(i, end - start))
                    print("---------------------------")
                    if i != iter - 1:
                        self.tearDown()

            return wrapper

        return time_recorder

    #
    # def test_text(self):
    #     text_question = "Who was the first President of USA?"
    #     self.say(text_question)
    #
    #     # check if response about President
    #     cortana_response = self.driver.find_element_by_class_name("TextBlock").text
    #     self.assertIn("president", cortana_response, "Search not about President")
    #
    #     # check if result correct President
    #     cortana_result = self.get_screenshot_text(area=(45, 735, 340, 55))
    #     woflram_result = self.get_woflramalpha_result(text_question)
    #     self.assertIn(cortana_result, woflram_result, "Result not correct")
    #
    # def test_weather(self):
    #     text_city = "weather in Vinnytsya"
    #     self.say(text_city)
    #
    #     # check if response about weather
    #     cortana_response = self.get_screenshot_text(area=(50, 471, 340, 30))
    #     self.assertTrue(self.check_response(text_city, cortana_response), "Search not about weather")
    #
    #     # check if correct city selected
    #     cortana_result = self.get_screenshot_text(area=(50, 525, 160, 31))
    #     self.assertTrue(self.check_response(text_city, cortana_result), "Incorrect city")
    #
    # def test_calculator(self):
    #     text_math = "2 multiply by 18 equal"
    #     math_actual = 2 * 18
    #     self.say(text_math)
    #
    #     # check if response about calculation
    #     cortana_response = self.driver.find_element_by_class_name("WebView").text
    #     # self.assertIn(text_math, cortana_response, "Text '{0}' not in Cortana response".format(text_math))
    #     self.assertTrue(self.check_response(text_math, cortana_response), "Search not about calculator")
    #
    #     # check if correct calculation
    #     cortana_result = self.driver.find_element_by_accessibility_id("rcHead").text
    #     self.assertEqual(str(math_actual), cortana_result, "{0} don't equal {1}".format(math_actual, cortana_result))
    #
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
    #     print(cortana_result)

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

    @monitor(iter=4)
    def test_performance_1(self):
        self.say("What time is it?", 5)


unittest.main()
