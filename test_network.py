import time

import psutil

# subprocess.call("wmic path win32_networkadapter where index=1 call enable")

for i in range(10):
    for process in psutil.process_iter():
        if process.name() == "SearchUI.exe":
            with process.oneshot():
                print(process.name())
                print(process.memory_info().rss / (1024 * 1024))
                print(process.memory_info().vms / (1024 * 1024))
                print(process.cpu_percent(interval=1))
                print("-----------------------------")
    time.sleep(1)
