import threading
import time


# subprocess.call("wmic path win32_networkadapter where index=1 call enable")

class Waiter(threading.Thread):
    def __init__(self, name, count):
        threading.Thread.__init__(self)
        self.name = name
        self.count = count

    def run(self):
        for i in range(self.count):
            print(f"This is {self.name}")
            time.sleep(1)
