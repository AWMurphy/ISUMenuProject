from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


driver = webdriver.Edge()  # or webdriver.Firefox()
driver.get("https://www.dining.iastate.edu/hours-menus/")
time.sleep(4)
continue_link = driver.find_element(By.LINK_TEXT, 'Memorial Union Food')
driver.execute_script("arguments[0].scrollIntoView();", continue_link)
continue_link.click()
time.sleep(2)

