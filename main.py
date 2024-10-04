from openPlaces import GetOpenRestaurants
from calories import PrintMenus
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

driver = webdriver.Edge()

with open('restarauntLinks.json') as json_file:
    links = json.load(json_file)

index = 0 #had to make this because of the apostrophe in Whirlybird's

#PrintMenus(driver, "https://www.dining.iastate.edu/location/whirlybird")
#PrintMenus(driver, links["Roasterie"])

places = GetOpenRestaurants(driver)
print(places)

for place in places:
    print(links[place])
    link = links[place]
    PrintMenus(driver, link)

driver.quit()