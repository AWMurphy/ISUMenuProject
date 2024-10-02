from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

def GetOpenRestaurants():
    driver = webdriver.Edge()  # or webdriver.Firefox()
    driver.get("https://www.dining.iastate.edu/hours-menus")
    element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div/span[2]')
    elementHTML = element.get_attribute('innerHTML')
    element.click()
    time.sleep(5)

    element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div/div[1]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[55]')
    element.click()
    time.sleep(5)

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