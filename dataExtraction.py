import json
import requests
import sys

def extract_food_data(response_data):
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


                    # diet variables
                    isHalal = 0
                    isVegan = 0
                    isVegetarian = 0

                    # allergen variables
                    containsDairy = 0
                    containsEgg = 0
                    containsFish = 0
                    containsPeanuts = 0
                    containsShellfish = 0
                    containsSoy = 0
                    containsSesame = 0
                    containsTreeNuts = 0
                    containsWheatGluten = 0

                    # extract the traits
                    traits = item_info.get("traits", {}) # this will never hit the {} because the null in the

                    if traits != None and traits != {}:
                        # extract the diets
                        diets = traits.get("requirement", [])

                        # ensure safety by lowercasing them
                        diets_lower = []

                        if isinstance(diets, dict):
                            for number, diet in enumerate(diets): # enumerate most likely useless because of the .append change
                                diets_lower.append(str(diet).lower())
                        else:
                            diets_lower = []

                        if "halal" in diets_lower:
                            isHalal = 1
                        if "vegan" in diets_lower:
                            isVegan = 1
                        if "vegetarian" in diets_lower:
                            isVegetarian = 1

                        # extract the allergens
                        allergens = traits.get("allergen", [])

                        # ensure safety by lowercasing them
                        allergens_lower = []

                        if isinstance(allergens, dict):
                            for number, allergen in enumerate(allergens):
                                allergens_lower.append(str(allergen).lower())
                        else:
                            allergens_lower = []

                        if "dairy" in allergens_lower:
                            containsDairy = 1
                        if "egg" in allergens_lower:
                            containsEgg = 1
                        if "fish" in allergens_lower:
                            containsFish = 1
                        if "peanuts" in allergens_lower:
                            containsPeanuts = 1
                        if "shellfish" in allergens_lower:
                            containsShellfish = 1
                        if "soy" in allergens_lower:
                            containsSoy = 1
                        if "sesame_tahini" in allergens_lower:
                            containsSesame = 1
                        if "wheat_gluten" in allergens_lower:
                            containsWheatGluten = 1
                        if "tree_nuts" in allergens_lower:
                            containsTreeNuts = 1
                    
                    # save the data to our dictionary which is our database data / database json
                    extracted_database[outer_id] = {
                        "name": food_name,
                        "time_of_day": time_of_day,
                        "calories": calories,
                        "calorieError": calError,
                        "category": food_category,
                        "station": food_station,
                        "venue": food_venue,
                        "isHalal": isHalal,
                        "isVegan": isVegan,
                        "isVegetarian": isVegetarian,
                        "containsDairy": containsDairy,
                        "containsEggs": containsEgg,
                        "containsFish": containsFish,
                        "containsPeanuts": containsPeanuts,
                        "containsShellfish": containsShellfish,
                        "containsSoy": containsSoy,
                        "containsSesame": containsSesame,
                        "containsTreeNuts": containsTreeNuts,
                        "containsWheatGluten": containsWheatGluten
                    }

    return extracted_database

# for context, all 3 functions are the same, this is just in case they ever change just ONE of the json requests for any reason