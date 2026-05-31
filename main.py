# imports I'm using
import requests
import json
import os
import datetime

# using defs from other files to keep code clean
import dataExtraction
import dataDatabase

# construct the file path (go up one folder in the warren rework folder)
filePath = os.path.join('Warren_Rework', 'DiningHallLinks.json')

# load the updated links via the dining hall links json
with open(filePath) as json_file:
    links = json.load(json_file)

# user-agent so that the api request actually thinks an actual person is trying to get access, accept is the return type (a json type)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    "Accept": "application/json"
}

# the URL uses todays date for the request
today = datetime.date.today()

for place, url in links.items():
    print(f"Fetching data for: {place}")
    try:
        response = requests.get(url + today.strftime("%Y-%m-%d"), headers=headers) # use the headers above along with the url from the dining halls json

        if response.status_code == 200:

            if place == "Friley Windows":
                menu_json = response.json()

                """
                with open('output.txt', 'w') as f:
                    print(json.dumps(menu_json, indent=4), file=f) # json.dumps() used to clean print the information
                """

                finalizedData = dataExtraction.extract_food_data(menu_json)

                with open('FW.txt', 'w') as t:
                    print(json.dumps(finalizedData, indent=4), file=t)

                dataDatabase.save_to_database_per_location(finalizedData, place)

            elif place == "Seasons Marketplace":
                menu_json = response.json()
                
                finalizedData = dataExtraction.extract_food_data(menu_json)

                with open('SM.txt', 'w') as t:
                    print(json.dumps(finalizedData, indent=4), file=t)

                dataDatabase.save_to_database_per_location(finalizedData, place)

            elif place == "Union Drive Marketplace":
                menu_json = response.json()

                finalizedData = dataExtraction.extract_food_data(menu_json)
            
                with open('UDCC.txt', 'w') as t:
                    print(json.dumps(finalizedData, indent=4), file=t)

                dataDatabase.save_to_database_per_location(finalizedData, place)

            else:

                print("Correctly obtained!") # should never run

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}") # since this should always return status code 200, if the response doesn't understand that it's wrong
            print("Response content snippet:", response.text[:200]) # see the first 200 characters of what it sent back

    except json.JSONDecodeError:
        print("The response was not valid JSON.")
        print("Received content:", response.text[:200]) # show the first 200 characters of the errors so you can check what the problem might be