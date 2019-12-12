import time

import selenium.webdriver as webdriver

import processes as pc

# SEARCH_BOX_LOCATOR = "[class^='theme__inputElement']"
GOOGLE_URL = "https://www.google.com/"

monitor = pc.Monitor("chromedriver.exe")


def go_to(text):
    time_go = 2

    driver = webdriver.Chrome("resources/chromedriver.exe")
    monitor.csv_write(monitor.get_process_stat())
    driver.get(GOOGLE_URL)
    monitor.csv_write(monitor.get_process_stat())
    element = driver.find_element_by_name("q")
    monitor.csv_write(monitor.get_process_stat())
    element.send_keys(text)
    monitor.csv_write(monitor.get_process_stat())
    element.submit()

    for num in range(time_go):
        list_elements = driver.find_elements_by_css_selector("div.r > a:first-child")
        list_elements[num].click()
        driver.execute_script("window.history.go(-1)")
        time.sleep(1)
    # search_box_element = driver.find_element_by_css_selector(SEARCH_BOX_LOCATOR)


go_to("Joker")
