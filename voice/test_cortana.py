import time
import unittest

import pyttsx3
import uiautomation as auto

TEXT = "Weather in Vinnytsya"
BROWSER = "Open microsoft.com"


class Test_Cortana(unittest.TestCase):
    def setUp(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 100)
        self.open_cortana()

    def tearDown(self):
        self.engine.runAndWait()
        time.sleep(1)
        self.get_control()

    def open_cortana(self):
        self.engine.say("Hey Cortana")

    def get_control(self):
        control = auto.GetFocusedControl()
        control_list = []
        while control:
            control_list.insert(0, control)
            control = control.GetParentControl()
        print(control_list)

    def test_text(self):
        text = "Who was the first president of USA?"
        self.engine.say(text)

    # def test_calculator(self):
    #     calculation = "2*18="
    #     self.engine.say(calculation)


unittest.main()
