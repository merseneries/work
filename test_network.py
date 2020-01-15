from multiprocessing import Process
from monitor import Monitor
import time
import datetime
import psutil
import re
import subprocess


# subprocess.call("wmic path win32_networkadapter where index=1 call enable")

class Volume:
    PATH = r"E:\PycharmProjects\TestBad\resources\programs\SetVol.exe "
    REPORT = "report"

    def __init__(self):
        self.level = self.get_level()

    def get_level(self):
        result = subprocess.check_output(self.PATH + self.REPORT).decode("utf-8")
        current_volume = re.search(r"\d+", result)
        return current_volume.group()

    def set_volume(self, number):
        subprocess.call(self.PATH + str(number))

    def decrease(self, number):
        subprocess.call(self.PATH + "-" + str(number))

    def increase(self, number):
        subprocess.call(self.PATH + "+" + str(number))

    def mute(self):
        subprocess.call(self.PATH + "mute")

    def unmute(self):
        subprocess.call(self.PATH + "unmute")


volume = Volume()
volume.increase(50)
