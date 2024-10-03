from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# adding for testing cases of try statement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def GetOpenRestaurants():
    driver = webdriver.Edge()  # or webdriver.Firefox() / assigning our driver to Microsoft Edge
    driver.get("https://www.dining.iastate.edu/hours-menus")
    element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div/span[2]') # clicking the open now button
    elementHTML = element.get_attribute('innerHTML')
    element.click()
    time.sleep(2)

    try:
    # finding the element we wanna click
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.XPATH, '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[55]'))
        )

        # element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[55]') < isn't needed
        element.click()
        time.sleep(5)

        print("Element is clickable.")

        element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[2]/div[2]')
        elementHTML = element.get_attribute('innerHTML')
        time.sleep(2)

    except ElementClickInterceptedException:
        print("Element is not clickable because another element is obstructing it.")

        # Find the element you want to scroll to: in this case its about 12:30 so that 1:30 is still visible
        element2 = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[53]')
        time.sleep(2)

        # Scroll the page until the element is in view: scrolls down to 12:30, 1:30 should still be visible
        driver.execute_script("arguments[0].scrollIntoView();", element2)
        time.sleep(2)

        element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[55]')
        element.click()
        time.sleep(2)

        element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[2]/div[2]')
        elementHTML = element.get_attribute('innerHTML')
        time.sleep(2)

    #print(elementHTML)
    soup = BeautifulSoup(elementHTML, 'lxml')

    # Find all resteraunt headers
    places = soup.find_all('div', class_='mh-listing--description-header')

    #Create new soup to get names of places from
    soup = BeautifulSoup(str(places), 'lxml') 

    # Find all the h3 tags (have the actual name)
    h3_tags = soup.find_all('h3')

    # Loop through and print the content inside each h3 tag
    restaurants = []

    for tag in h3_tags:
        restaurants.append(tag.text.strip())
        #print(tag.text.strip())  # Use .strip() to clean up extra spaces or newlines

    driver.quit()

    return restaurants

print(GetOpenRestaurants())