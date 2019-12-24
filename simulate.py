import re

import pyautogui as autogui
import uiautomation as auto


def convert_to_digit(string):
    value = re.sub(r"\s", "", string)
    return float(value.replace(",", ".")) if "," in value else int(value)


def calcul_check():
    autogui.press("win")
    autogui.write("calculator")
    autogui.press("enter", pause=1)
    autogui.write("1003,5+2=")

    control = auto.GetFocusedControl()
    control_list = []
    while control:
        control_list.insert(0, control)
        control = control.GetParentControl()

    text = control_list[-1].Name[11:]
    result = convert_to_digit(text)
    print(result)


# title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
# print(title)
# control = win32gui.FindWindowEx(title, 0, "", None)
# print("text: ", win32gui.GetWindowText(control))

calcul_check()
