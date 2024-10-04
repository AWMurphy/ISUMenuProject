from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


#driver = webdriver.Edge()  # or webdriver.Firefox()


def PrintMenus(Driver, link):
    index = 6

    driver = Driver

    driver.get(link)

    failed = False
    while (failed == False):
        try:
            element = driver.find_element("xpath", '//*[@id="hours-and-menus"]/div/div[2]/div/div/div[4]/div[' + str(index) + ']') #xpath is to the visible menu, need to click on lunch and dinner to get those to work
            elementHTML = element.get_attribute('innerHTML')

            soup = BeautifulSoup(elementHTML, 'lxml')

            # Extract specific information, e.g., menu items, calories, and categories
            items = soup.find_all('li', class_='mh-location--single-menu--item')
            for item in items:
                name = item.find('span', class_='mh-menu-item-name').text
                try:
                    calories = item.find('span', class_='mh-menu-item-calories').text
                except:
                    calories = None
                categories = item.find_all('span', class_='mh-menu-item-category')
                category_list = [category['aria-label'] for category in categories]
                
                print(f'Item: {name}, Calories: {calories}, Categories: {category_list}')
        except:
            failed = True
        index += 1
        print(" ")

