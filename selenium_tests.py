import time

import selenium.webdriver as webdriver

import processes as pc

# SEARCH_BOX_LOCATOR = "[class^='theme__inputElement']"
GOOGLE_URL = "https://www.google.com/"

monitor = pc.Monitor("chromedriver.exe")


def go_to(text):
    time_go = 2

    driver = webdriver.Chrome("resources/chromedriver.exe")
    driver.get(GOOGLE_URL)
    monitor.get_now()
    element = driver.find_element_by_name("q")
    element.send_keys(text)
    element.submit()
    monitor.get_now()

    for num in range(time_go):
        time.sleep(1)
        list_elements = driver.find_elements_by_css_selector("div.r > a:first-child")
        list_elements[num].click()
        driver.execute_script("window.history.go(-1)")
        monitor.get_now()

        monitor.get_now()
    monitor.csv_write(monitor.data, mode="a")


go_to("Joker")
