import allure_pytest

PATH = r"E:\Programs\WindowsApplicationDriver\WinAppDriver.exe"
import sys
import os

PATH_CORTANA = r"C:\Windows\SystemApps\Microsoft.Windows.Cortana_cw5n1h2txyewy\SearchUI.exe"

os.startfile(PATH_CORTANA)

# subprocess.call("wmic path win32_networkadapter where index=1 call enable")
