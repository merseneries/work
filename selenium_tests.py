import selenium.webdriver as webdriver


SEARCH_BOX_LOCATOR = "[class^='theme__inputElement']"

driver = webdriver.Chrome("resources/chromedriver.exe")
driver.get("https://weather.com/")
search_box_element = driver.find_element_by_css_selector(SEARCH_BOX_LOCATOR)

print("wait")
# driver.close()
