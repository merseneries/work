import datetime
import time
import unittest
import pyautogui as autogui
import pytesseract
import pyttsx3
import re
import os
import sys
import pytz
import pytest
import selenium
import wolframalpha
import allure
from appium import webdriver

sys.path.append(r"E:\PycharmProjects\TestBad")
from local_package.monitor import Monitor
from local_package.funcs import Volume, Process, csv_write

BROWSER = "Open microsoft.com"
PATH_CORTANA = r"C:\Windows\SystemApps\Microsoft.Windows.Cortana_cw5n1h2txyewy\SearchUI.exe"
PATH_ALARM = r"E:\PycharmProjects\TestBad\resources\Alarm.lnk"
PATH_WIN_DRIVER = r"E:\Programs\WindowsApplicationDriver\WinAppDriver.exe"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

autogui.FAILSAFE = False
counter_test = 0
field_names = ["Test case ID", "Description", "Command", "Expected result",
               "Pass/Fail", "Time to execute", "Error message"]


class Test_Cortana(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.command = ""
        self.expected_result = ""
        self.tests_result = []
        desired_caps = {"app": PATH_CORTANA}

        os.startfile(PATH_WIN_DRIVER)
        autogui.hotkey("win", "c")
        self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities=desired_caps)

        autogui.press("esc")
        self.monitor = Monitor("SearchUI.exe")

    @classmethod
    def tearDownClass(self):
        self.driver.quit()
        self.tests_result.insert(0, field_names)
        csv_write("tests_result", self.tests_result)
        Process.kill("SearchUI.exe")
        Process.kill("WinAppDriver.exe")

    def setUp(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 110)
        self.say("Hey Cortana")
        print("Opening...")
        self.check_cortana()

    def tearDown(self):
        autogui.press("esc")
        if self.is_exist("Close"):
            self.driver.find_element_by_name("Close").click()
            print("Closed with find element")
        print("Closed...")

    def open_cortana(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 110)
        self.say("Hey Cortana")

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

    def check_cortana(self):
        try:
            self.driver.find_element_by_accessibility_id("TipTextBlock")
        except Exception:
            autogui.hotkey("win", "c")
            print("Pressed hotkeys for open Cortana")

    def is_exist(self, name):
        try:
            result = self.driver.find_element_by_name(name)
        except selenium.common.exceptions.NoSuchElementException:
            return False
        except selenium.common.exceptions.NoSuchWindowException:
            return False
        return result

    def monitor(iter=1, monitor_on=False):
        def time_recorder(func):
            def wrapper(self):
                error_msg = "-"
                for i in range(iter):
                    if i != 0:
                        self.setUp()
                    if monitor_on:
                        self.monitor.begin()

                    start = time.time()
                    try:
                        func(self)
                    except Exception as error:
                        error_msg = error
                        # raise error
                    end = time.time()

                    if monitor_on:
                        self.monitor.end()
                    if i != iter - 1:
                        self.tearDown()

                    global counter_test
                    counter_test = counter_test + 1
                    test_result = "Pass" if error_msg == "-" else "Fail"
                    time_spend = round(end - start, 3)
                    error_msg = str(error_msg).replace("\n", "")

                    # print("---------------------------")
                    print("Number of test #" + str(counter_test))
                    # print("Description:", func.__name__)
                    # print("Command:", self.command)
                    # print("Expected result:", self.expected_result)
                    # print("Error:", error_msg)
                    # print("Test result:", test_result)
                    # print("Time spend:", time_spend)
                    # print("---------------------------")

                    self.tests_result.append([counter_test, func.__name__, self.command,
                                              self.expected_result, test_result, time_spend, error_msg])

            return wrapper

        return time_recorder

    """

    ###------------------Smoke tests------------------###

    """

    # # Say 'Hey Cortana' to check if it opened
    # @monitor(iter=1)
    # def test_smoke_1(self):
    #     self.command = "Hey Cortana"
    #     cortana_response = self.driver.find_element_by_name("Cortana").text
    #     self.expected_result = "Cortana"
    #     self.assertEqual(cortana_response, self.expected_result, "Cortana doesn't open")
    #
    # @monitor(iter=1)
    # def test_smoke_2(self):
    #     text_time = "What time is it?"
    #     self.say(text_time)
    #     self.command = text_time
    #     cortana_response = self.get_screenshot_text(area=(150, 560, 200, 50))
    #     current_time = time.strftime(" %I:%M %p").lstrip(" 0").replace("0", "")
    #     self.expected_result = current_time
    #     self.assertEqual(cortana_response, current_time, "Time doesn't equal")
    #
    # @monitor(iter=1)
    # def test_smoke_3(self):
    #     text_open = "Open settings"
    #     self.say(text_open)
    #     self.command = text_open
    #     cortana_response = self.get_screenshot_text(area=(50, 450, 325, 60))
    #     self.expected_result = text_open
    #     self.assertTrue(self.check_response(text_open, cortana_response), "Setting didn't open")
    #
    # @monitor(iter=1)
    # def test_smoke_4(self):
    #     self.say("", 15)
    #     check_exist = self.is_exist("Cortana")
    #     self.assertFalse(check_exist, "Cortana didn't close after say nothing")
    #
    # @monitor(iter=1)
    # def test_smoke_5(self):
    #     self.say("Грай музику", 15)
    #     check_exist = self.is_exist("Cortana")
    #     self.assertFalse(check_exist, "Cortana didn't close")

    """
    
    ###------------------Functionality tests------------------###
    
    """

    #
    # @allure.step("Test set alarm and check if it opened")
    # @monitor(iter=1)
    # def test_alarm_set(self):
    #     text_alarm = "Set alarm tomorrow at 11 am"
    #     self.command = text_alarm
    #     self.say(text_alarm, 4)
    #
    #     # check if response about set alarm
    #     cortana_response = self.get_screenshot_text(area=(55, 560, 150, 55))
    #     self.expected_result = text_alarm
    #     self.assertTrue(self.check_response(text_alarm, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_alarm, cortana_response))
    #
    #     # add check if system set alarm in app
    #     Process.open(PATH_ALARM)
    #     check_open = Process.is_alive("Time.exe")
    #     self.expected_result = True
    #     self.assertTrue(check_open, "Alarm didn't open")
    #
    #     autogui.hotkey("win", "c")
    #     self.say("Delete all alarms")
    #     autogui.sleep(2)
    #     Process.kill("Time.exe")
    #
    # @allure.step("Test check calculator operation")
    # @monitor(iter=1)
    # def test_calculator_operation(self):
    #     text_math = "2 multiply by 18 equal"
    #     math_expected = 2 * 18
    #     self.command = text_math
    #
    #     self.say(text_math)
    #
    #     # check if response about calculation
    #     cortana_response = self.driver.find_element_by_class_name("WebView").text
    #     self.expected_result = text_math
    #     self.assertTrue(self.check_response(text_math, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_math, cortana_response))
    #
    #     # check if correct calculation
    #     cortana_result = self.driver.find_element_by_accessibility_id("rcHead").text
    #     self.expected_result = math_expected
    #     self.assertEqual(str(math_expected), cortana_result,
    #                      "{0} don't equal {1}".format(math_expected, cortana_result))
    #
    # @allure.step("Test check how much seconds in week")
    # @monitor(iter=1)
    # def test_converter_week(self):
    #     text_convert = "How much seconds in week"
    #     expected_convert = str(7 * 24 * 60 * 60)
    #     self.command = text_convert
    #
    #     self.say(text_convert)
    #
    #     # check if response about convert
    #     cortana_response = self.get_screenshot_text(area=(55, 532, 100, 25))
    #     self.expected_result = text_convert
    #     self.assertTrue(self.check_response(text_convert, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_convert, cortana_response))
    #
    #     # check if correct convert result
    #     cortana_result = self.get_screenshot_text(area=(55, 561, 121, 30))
    #     self.expected_result = expected_convert
    #     self.assertEqual(expected_convert, cortana_result,
    #                      "{0} don't equal {1}".format(expected_convert, cortana_result))
    #
    #     autogui.sleep(2)
    #
    # @allure.step("Test check image of dogs")
    # @monitor(iter=1)
    # def test_image_search(self):
    #     text_image = "Show images of dogs"
    #     self.command = text_image
    #     self.say(text_image)
    #
    #     # check if response about image
    #     cortana_response = self.driver.find_element_by_accessibility_id("GreetingLine1").text
    #     self.expected_result = text_image
    #     self.assertTrue(self.check_response(text_image, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_image, cortana_response))
    #
    # @allure.step("Test check if calendar opened")
    # @monitor(iter=1)
    # def test_open_calendar(self):
    #     text_open = "calendar"
    #     self.command = text_open
    #     self.say(text_open)
    #
    #     # check if response about calendar
    #     cortana_response = self.get_screenshot_text(area=(50, 500, 325, 60))
    #     self.expected_result = text_open
    #     self.assertTrue(self.check_response(text_open, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_open, cortana_response))
    #     self.wait_listen()
    #     self.say(text_open, 7)
    #
    #     # check if correct program opened
    #     # cortana_result = self.get_screenshot_text(area=(60, 505, 325, 40))
    #     # self.assertTrue(self.check_response(text_open, cortana_result), "Must opened calendar")
    #
    #     calendar_opened = Process.is_alive("OUTLOOK.EXE")
    #     self.expected_result = True
    #     self.assertTrue(calendar_opened, "Outlook didn't open")
    #     Process.kill("OUTLOOK.EXE")
    #
    # @allure.step("Test say question and check response")
    # @monitor(iter=1)
    # def test_some_question(self):
    #     text_question = "Who is the first President of USA?"
    #     self.command = text_question
    #     self.say(text_question)
    #
    #     # check if response about President
    #     cortana_response = self.driver.find_element_by_accessibility_id("GreetingLine1").text
    #     self.expected_result = text_question
    #     self.assertTrue(self.check_response(text_question, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_question, cortana_response))
    #
    #     # check if result correct President
    #     cortana_result = self.get_screenshot_text(area=(178, 600, 200, 40))
    #     woflram_result = self.get_woflramalpha_result(text_question).split(" (", 1)[0]
    #     self.expected_result = woflram_result
    #     self.assertEqual(cortana_result, woflram_result, "Result not correct")
    #
    # @allure.step("Test decrease volume")
    # @monitor(iter=1)
    # def test_volume_sound(self):
    #     volume = Volume()
    #     start_level = volume.get_level()
    #
    #     text_volume = "Decrease volume by 30"
    #     self.command = text_volume
    #     self.say(text_volume)
    #     changed_level = volume.get_level()
    #
    #     self.expected_result = changed_level
    #     self.assertNotEqual(start_level, changed_level, "Volume didn't change")
    #
    #     # autogui.press("volumedown", presses=4)
    #     volume.set_volume(100)
    #
    # @allure.step("Test open excel")
    # @monitor(iter=1, monitor_on=True)
    # def test_open_excel(self):
    #     excel_process = "EXCEL.EXE"
    #
    #     text_open = "Open excel"
    #     self.command = text_open
    #     self.say(text_open)
    #
    #     # check if response about excel
    #     # cortana_response = self.get_screenshot_text(area=(50, 490, 150, 50))
    #     # self.expected_result = text_open
    #     # self.assertTrue(self.check_response(text_open, cortana_response),
    #     #                 "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_open, cortana_response))
    #
    #     time.sleep(3)
    #     # check if excel opened
    #     self.expected_result = True
    #     self.assertTrue(Process.is_alive(excel_process), "Excel didn't open")
    #
    #     Process.kill(excel_process)

    @monitor(iter=100, monitor_on=True)
    def test_open_chrome(self):
        chrome_process = "chrome.exe"

        text_open = "Open Chrome"
        self.command = text_open
        self.say(text_open, 8)

        # check if response about excel
        # cortana_response = self.get_screenshot_text(area=(50, 490, 150, 50))
        # self.expected_result = text_open
        # self.assertTrue(self.check_response(text_open, cortana_response),
        #                 "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_open, cortana_response))

        # check if chrome opened
        self.expected_result = True
        self.assertTrue(Process.is_alive(chrome_process), "Chrome didn't open")

        Process.kill(chrome_process)
        time.sleep(1)
        self.assertFalse(Process.is_alive(chrome_process), "Chrome didn't close")

    #
    # @allure.step("Test check what time in Tokyo")
    # @monitor(iter=1)
    # def test_time_city(self):
    #     text_time = "What time in Tokyo?"
    #     self.command = text_time
    #     self.say(text_time, 4)
    #
    #     # check if response about time
    #     cortana_response = self.driver.find_element_by_accessibility_id("GreetingLine1").text
    #     self.expected_result = text_time
    #     self.assertTrue(self.check_response(text_time, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_time, cortana_response))
    #
    #     cortana_result = self.get_screenshot_text(area=(150, 560, 200, 80)).replace("\n\n", " ")
    #     expected_tokyo = datetime.datetime.now(pytz.timezone("Asia/Tokyo")) \
    #         .strftime(" %I:%M %p %a, %b %d, %Y").replace(" 0", "")
    #     expected_tokyo = expected_tokyo[1:] if expected_tokyo[0] == " " else expected_tokyo
    #     self.expected_result = expected_tokyo
    #     self.assertEqual(expected_tokyo, cortana_result, "Result doesn't equal")
    #
    # @allure.step("Test check weather in Vinnytsya")
    # @monitor(iter=1)
    # def test_weather_city(self):
    #     text_city = "weather in Vinnytsya"
    #     self.command = text_city
    #     self.say(text_city, 4)
    #
    #     # check if response about weather
    #     cortana_response = self.get_screenshot_text(area=(50, 471, 340, 30))
    #     self.expected_result = text_city
    #     self.assertTrue(self.check_response(text_city, cortana_response),
    #                     "Search not correct. Expected: '{}'. Actual: '<{}>'".format(text_city, cortana_response))
    #
    #     # check if correct city selected
    #     cortana_result = self.get_screenshot_text(area=(50, 525, 160, 31)).split(",")[0]
    #     text_city = text_city.split(" ")[-1]
    #     self.expected_result = text_city
    #     self.assertTrue(self.check_response(text_city, cortana_result),
    #                     "Incorrect city. Expected: '{}'. Actual: '<{}>'".format(text_city, cortana_result))
    #
    # @allure.step("Test open and play music")
    # @monitor(iter=1)
    # def test_music(self):
    #     text_music = "Open Groove music"
    #     self.command = text_music
    #     self.say(text_music, 6)
    #
    #     autogui.press("enter")
    #     actual_open = Process.is_alive("Music.UI.exe")
    #     self.expected_result = True
    #     self.assertTrue(actual_open, "Music didn't open")
    #
    #     autogui.sleep(3)
    #     Process.kill("Music.UI.exe")
    #
    # @allure.step("Test open Movies & TV and play movie")
    # @monitor(iter=1)
    # def test_movie(self):
    #     text_movie = "Open Movies & TV"
    #     self.command = text_movie
    #     self.say(text_movie, 6)
    #
    #     autogui.press("enter")
    #     autogui.sleep(1)
    #     autogui.press("enter")
    #     actual_open = Process.is_alive("Video.UI.exe")
    #     self.expected_result = True
    #     self.assertTrue(actual_open, "Video didn't open")
    #
    #     autogui.sleep(3)
    #     Process.kill("Video.UI.exe")
    #
    # # def test_email(self):
    # #     text_email = "Send email to Jared about What you will do tomorrow?"
    # #     self.say(text_email)
    #
    # # def test_translate(self):
    # #     text_translate = "Translate extraordinary human to ukrainian"
    # #     self.say(text_translate)
    # #
    # #     # check if correct response
    # #     # cortana_result = self.get_screenshot_text(area=(60, 710, 200, 45))
    # #     # self.assertEqual("надзвичайна людина", cortana_result, "Translate incorrect")
    #
    # # def test_route(self):
    # #     text_route = "Show me route from London to Berlin"
    # #     self.say(text_route)
    #
    # # def test_video(self):
    # #     text_time = "Play video in YouTube about Iron man"
    # #     self.say(text_time)

    """

    ###------------------Performance tests------------------###

    """

    # @monitor(iter=4)
    # def test_performance_1(self):
    #     self.say("What time is it?", 5)

    """

    ###------------------UI tests------------------###

    """


if __name__ == '__main__':
    unittest.main()
