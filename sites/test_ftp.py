import os
import time
from ftplib import FTP

import pyautogui

ROOT = os.path.normpath(os.getcwd() + os.sep + os.pardir)
HOST = "ftp.bohdan.vincity.net"
USERNAME = "bohdan"
PASSWORD = "4P4j3I5l"


def get_img_path():
    current_time = str(int(time.time()))
    file_name = "img_" + current_time + ".png"
    file_path = ROOT + os.sep + "resources"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path + os.sep + file_name, file_name


def ftp_upload(host, username, password):
    ftp = FTP(host, username, password)
    ftp.cwd("Screenshots")
    # ftp.login()

    file_path, file_name = get_img_path()
    pyautogui.screenshot().save(file_path)

    with open(file_path, 'rb') as file:
        ftp.storbinary('STOR ' + file_name, file, 1024)

    ftp.quit()


ftp_upload(HOST, USERNAME, PASSWORD)
