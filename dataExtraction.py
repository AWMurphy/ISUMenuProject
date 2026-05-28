import json
import requests

def extract_food_data_FW(response_data):
    """
    Parses the ISU dining JSON and extracts items by their outer ID,
    capturing the name, time of day (meal), and calories + any other parts of the JSON that seem necessary.
    """
    extracted_database = {}

    # loop through the meals (e.g., Breakfast, Lunch, Dinner), Using .get("meals", {}) prevents crashes if the "meals" key is missing
    for meal_key, meal_info in response_data.get("meals", {}).items():
        time_of_day = meal_info.get("meal", "Unknown").lower() # e.g., "lunch"
        
        # loop through the different stations/displays (e.g., "Savor", "Salad Bar")
        for display_key, display_info in meal_info.get("menu_displays", {}).items():
            
            # loop through categories (e.g., "entree", "sides")
            for category_key, category_info in display_info.get("categories", {}).items():
                
                # loop through the actual food items! ^ 'outer_id' will be keys like "281561902"
                for outer_id, item_info in category_info.get("items", {}).items():

                    print(f'Doing outer_id: {outer_id}')
                    
                    food_name = item_info.get("name", "Unknown Item")

                    print(f'Doing the item: {food_name}')

                    # skip if the item has a "--" at the start, means its a bar of some type, not a food item (maybe add this in later)
                    if (food_name[0:2] == "--"):
                        continue
                    
                    food_category = item_info.get("category_name")
                    food_station = item_info.get("serving_station")
                    food_venue = item_info.get("venue_name")

                    # extract calories (this assumes the JSON has a nutrients block) - use a try/except block just in case a food item (like water) has no calories listed
                    try:
                        calories = item_info["nutrients"]["kcal"]["quantity"]
                        calError = 0
                    except (KeyError, TypeError):
                        if TypeError:
                            calError = 1
                        calories = 0 
                    
                    # save the data to our dictionary which is our database data / database json
                    extracted_database[outer_id] = {
                        "name": food_name,
                        "time_of_day": time_of_day,
                        "calories": calories,
                        "calorieError": calError,
                        "category": food_category,
                        "station": food_station,
                        "venue": food_venue
                    }

    return extracted_database

def extract_food_data_SM(response_data):
    """
    Parses the ISU dining JSON and extracts items by their outer ID,
    capturing the name, time of day (meal), and calories + any other parts of the JSON that seem necessary.
    """
    extracted_database = {}

    # loop through the meals (e.g., Breakfast, Lunch, Dinner), Using .get("meals", {}) prevents crashes if the "meals" key is missing
    for meal_key, meal_info in response_data.get("meals", {}).items():
        time_of_day = meal_info.get("meal", "Unknown").lower() # e.g., "lunch"
        
        # loop through the different stations/displays (e.g., "Savor", "Salad Bar")
        for display_key, display_info in meal_info.get("menu_displays", {}).items():
            
            # loop through categories (e.g., "entree", "sides")
            for category_key, category_info in display_info.get("categories", {}).items():
                
                # loop through the actual food items! ^ 'outer_id' will be keys like "281561902"
                for outer_id, item_info in category_info.get("items", {}).items():

                    print(f'Doing outer_id: {outer_id}')
                    
                    food_name = item_info.get("name", "Unknown Item")

                    print(f'Doing the item: {food_name}')

                    # skip if the item has a "--" at the start, means its a bar of some type, not a food item (maybe add this in later)
                    if (food_name[0:2] == "--"):
                        continue
                    
                    food_category = item_info.get("category_name")
                    food_station = item_info.get("serving_station")
                    food_venue = item_info.get("venue_name")

                    # extract calories (this assumes the JSON has a nutrients block) - use a try/except block just in case a food item (like water) has no calories listed
                    try:
                        calories = item_info["nutrients"]["kcal"]["quantity"]
                        calError = 0
                    except (KeyError, TypeError):
                        if TypeError:
                            calError = 1
                        calories = 0 
                    
                    # save the data to our dictionary which is our database data / database json
                    extracted_database[outer_id] = {
                        "name": food_name,
                        "time_of_day": time_of_day,
                        "calories": calories,
                        "calorieError": calError,
                        "category": food_category,
                        "station": food_station,
                        "venue": food_venue
                    }

    return extracted_database

def extract_food_data_UDCC(response_data):
    """
    Parses the ISU dining JSON and extracts items by their outer ID,
    capturing the name, time of day (meal), and calories + any other parts of the JSON that seem necessary.
    """
    extracted_database = {}

    # loop through the meals (e.g., Breakfast, Lunch, Dinner), Using .get("meals", {}) prevents crashes if the "meals" key is missing
    for meal_key, meal_info in response_data.get("meals", {}).items():
        time_of_day = meal_info.get("meal", "Unknown").lower() # e.g., "lunch"
        
        # loop through the different stations/displays (e.g., "Savor", "Salad Bar")
        for display_key, display_info in meal_info.get("menu_displays", {}).items():
            
            # loop through categories (e.g., "entree", "sides")
            for category_key, category_info in display_info.get("categories", {}).items():
                
                # loop through the actual food items! ^ 'outer_id' will be keys like "281561902"
                for outer_id, item_info in category_info.get("items", {}).items():

                    print(f'Doing outer_id: {outer_id}')
                    
                    food_name = item_info.get("name", "Unknown Item")

                    print(f'Doing the item: {food_name}')

                    # skip if the item has a "--" at the start, means its a bar of some type, not a food item (maybe add this in later)
                    if (food_name[0:2] == "--"):
                        continue
                    
                    food_category = item_info.get("category_name")
                    food_station = item_info.get("serving_station")
                    food_venue = item_info.get("venue_name")

                    # extract calories (this assumes the JSON has a nutrients block) - use a try/except block just in case a food item (like water) has no calories listed
                    try:
                        calories = item_info["nutrients"]["kcal"]["quantity"]
                        calError = 0
                    except (KeyError, TypeError):
                        if TypeError:
                            calError = 1
                        calories = 0 
                    
                    # save the data to our dictionary which is our database data / database json
                    extracted_database[outer_id] = {
                        "name": food_name,
                        "time_of_day": time_of_day,
                        "calories": calories,
                        "calorieError": calError,
                        "category": food_category,
                        "station": food_station,
                        "venue": food_venue
                    }

    return extracted_database

# for context, all 3 functions are the same, this is just in case they ever change just ONE of the json requests for any reason