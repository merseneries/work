import time
import unittest

import pyautogui as autogui
import pyttsx3
from appium import webdriver

BROWSER = "Open microsoft.com"
PATH_CORTANA = r"C:\Windows\SystemApps\Microsoft.Windows.Cortana_cw5n1h2txyewy\SearchUI.exe"
PATH_WINDRIVER = r"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"


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
        self.engine.setProperty('rate', 120)
        self.open_cortana()

    def tearDown(self):
        autogui.press("esc")

    def open_cortana(self):
        self.engine.say("Hey Cortana")

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

    def test_text(self):
        text_question = "Who was the first president of USA?"

        self.say(text_question)
        cortana_response = self.driver.find_element_by_class_name("TextBlock").text
        self.assertIn("president", cortana_response, "Search not about president")

    def test_weather(self):
        text_city = "weather in Vinnytsya"

        self.say(text_city)
        # cortana_response = self.driver.find_element_by_name("TextBlock").text

    def test_calculator(self):
        text_math = "2 asterisk 18 equal"
        math_actual = 2 * 18

        self.say(text_math)
        cortana_response = self.driver.find_element_by_class_name("WebView").text
        self.assertIn(text_math, cortana_response, "Text '{0}' not in Cortana response".format(text_math))

        cortana_answer = self.driver.find_element_by_accessibility_id("rcHead").text
        self.assertEqual(str(math_actual), cortana_answer, "{0} don't equal {1}".format(math_actual, cortana_answer))

    def test_open(self):
        text_open = "Calendar"

        self.say(text_open)
        cortana_response = self.driver.find_element_by_class_name("WebView").text
        self.assertIn(text_open, cortana_response,
                      "Trying to open '{0}' but response is '{1}'".format(text_open, cortana_response))
        self.wait_listen()
        self.say(text_open)


unittest.main()
