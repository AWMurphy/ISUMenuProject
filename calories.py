from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup


driver = webdriver.Edge()  # or webdriver.Firefox()
driver.get("https://www.dining.iastate.edu/location/friley-windows-2-2/")
element = driver.find_element("xpath", '/html/body/div/div/main/div/article/div/section/div[2]/div/div/div[2]/div/div/div[4]/div[8]/div[1]')
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
driver.quit()