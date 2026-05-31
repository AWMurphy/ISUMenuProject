import sqlite3
import discord

"""
Function that saves user data to the database.
If they are already in the database, updates the information.
"""
def save_user_data(user_id, username, selected_locations):

    # create or connect to our database
    conn = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursor = conn.cursor()

    # find the table name according to the location name, makes it safe for table names as well
    table_name = "user_data"

    # set all to 0 for now assuming they want none
    frileyWant = seasonsWant = UDCCwant = 0

    # below lines work on the incoming selected locations array, check each possible input to see what they selected
    if "Friley" in selected_locations:
        frileyWant = 1

    if "Seasons" in selected_locations:
        seasonsWant = 1

    if "UDCC" in selected_locations:
        UDCCwant = 1


    # create new table if it doesn't exist (shouldn't happen more than once)
    cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        user_id TEXT PRIMARY KEY,
                        username TEXT,
                        frileySelect INTEGER CHECK (frileySelect IN (0,1)),
                        seasonsSelect INTEGER CHECK (seasonsSelect IN (0,1)),
                        unionSelect INTEGER CHECK (unionSelect IN (0,1)),
                        halalDiet INTEGER CHECK (halalDiet IN (0,1)),
                        veganDiet INTEGER CHECK (veganDiet IN (0,1)),
                        vegetarianDiet INTEGER CHECK (vegetarianDiet IN (0,1)),
                        allergicDairy INTEGER CHECK (allergicDairy IN (0,1)),
                        allergicEggs INTEGER CHECK (allergicEggs IN (0,1)),
                        allergicFish INTEGER CHECK (allergicFish IN (0,1)),
                        allergicPeanuts INTEGER CHECK (allergicPeanuts IN (0,1)),
                        allergicShellfish INTEGER CHECK (allergicShellfish IN (0,1)),
                        allergicSoy INTEGER CHECK (allergicSoy IN (0,1)),
                        allergicSesame INTEGER CHECK (allergicSesame IN (0,1)),
                        allergicTreeNuts INTEGER CHECK (allergicTreeNuts IN (0,1)),
                        allergicWheatGluten INTEGER CHECK (allergicWheatGluten IN (0,1))
                    )
                    """)
    
    # insert new person or update person if the user_id is already in the table
    cursor.execute(f"""
                    INSERT INTO {table_name} (user_id, username, frileySelect, seasonsSelect, unionSelect,
                                              halalDiet, veganDiet, vegetarianDiet,
                                              allergicDairy, allergicEggs, allergicFish, allergicPeanuts,
                                              allergicShellfish, allergicSoy, allergicSesame, allergicTreeNuts, allergicWheatGluten) 
                    VALUES (?, ?, ?, ?, ?,
                            ?, ?, ?,
                            ?, ?, ?, ?,
                            ?, ?, ?, ?, ?) 
                    ON CONFLICT (user_id) DO UPDATE SET 
                    username = excluded.username,
                    frileySelect = excluded.frileySelect,
                    seasonsSelect = excluded.seasonsSelect,
                    unionSelect = excluded.unionSelect
                    """, 
                    (user_id, username, frileyWant, seasonsWant, UDCCwant,
                     0, 0, 0,
                     0, 0, 0, 0,
                     0, 0, 0, 0, 0))
    
    # commit changes
    conn.commit()
    
    # close the connection
    conn.close()

"""
Checks if the current person is in the database.
"""
def isInDatabase(user_id):

    # create or connect to our database
    conn = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursor = conn.cursor()

    # find the table name according to the location name, makes it safe for table names as well
    table_name = "user_data"

    # see if we can find 
    cursor.execute(f"""
                    SELECT * FROM {table_name}
                    WHERE user_id = {user_id}
                    """)
    
    # turn that into a list (it will be max 1, but 1 is still bigger than 0)
    hasInfo = cursor.fetchall()

    # assume we don't have a match
    doesExist = False

    # if hasInfo has a match, it's length will equal 1 or > 0
    if len(hasInfo) > 0:
        doesExist = True

    return doesExist

"""
Function that saves user diet data to the database.
If they are already in the database, updates the information.
"""
def save_user_diets(user_id, username, selected_diets):
    # create or connect to our database
    conn = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursor = conn.cursor()

    # find the table name according to the location name, makes it safe for table names as well
    table_name = "user_data"

    # set all to 0 for now assuming they want none
    halalDiet = veganDiet = vegetarianDiet = 0

    # below lines work on the incoming selected locations array, check each possible input to see what they selected
    if "Halal" in selected_diets:
        halalDiet = 1

    if "Vegan" in selected_diets:
        veganDiet = 1

    if "Vegetarian" in selected_diets:
        vegetarianDiet = 1


    # create new table if it doesn't exist (shouldn't happen more than once)
    cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        user_id TEXT PRIMARY KEY,
                        username TEXT,
                        frileySelect INTEGER CHECK (frileySelect IN (0,1)),
                        seasonsSelect INTEGER CHECK (seasonsSelect IN (0,1)),
                        unionSelect INTEGER CHECK (unionSelect IN (0,1)),
                        halalDiet INTEGER CHECK (halalDiet IN (0,1)),
                        veganDiet INTEGER CHECK (veganDiet IN (0,1)),
                        vegetarianDiet INTEGER CHECK (vegetarianDiet IN (0,1)),
                        allergicDairy INTEGER CHECK (allergicDairy IN (0,1)),
                        allergicEggs INTEGER CHECK (allergicEggs IN (0,1)),
                        allergicFish INTEGER CHECK (allergicFish IN (0,1)),
                        allergicPeanuts INTEGER CHECK (allergicPeanuts IN (0,1)),
                        allergicShellfish INTEGER CHECK (allergicShellfish IN (0,1)),
                        allergicSoy INTEGER CHECK (allergicSoy IN (0,1)),
                        allergicSesame INTEGER CHECK (allergicSesame IN (0,1)),
                        allergicTreeNuts INTEGER CHECK (allergicTreeNuts IN (0,1)),
                        allergicWheatGluten INTEGER CHECK (allergicWheatGluten IN (0,1))
                    )
                    """)
    
    # insert new person or update person if the user_id is already in the table
    cursor.execute(f"""
                    INSERT INTO {table_name} (user_id, username, frileySelect, seasonsSelect, unionSelect,
                                              halalDiet, veganDiet, vegetarianDiet,
                                              allergicDairy, allergicEggs, allergicFish, allergicPeanuts,
                                              allergicShellfish, allergicSoy, allergicSesame, allergicTreeNuts, allergicWheatGluten) 
                    VALUES (?, ?, ?, ?, ?,
                            ?, ?, ?,
                            ?, ?, ?, ?,
                            ?, ?, ?, ?, ?) 
                    ON CONFLICT (user_id) DO UPDATE SET 
                    username = excluded.username,
                    halalDiet = excluded.halalDiet,
                    veganDiet = excluded.veganDiet,
                    vegetarianDiet = excluded.vegetarianDiet
                    """, 
                    (user_id, username, 0, 0, 0,
                     halalDiet, veganDiet, vegetarianDiet,
                     0, 0, 0, 0,
                     0, 0, 0, 0, 0))
    
    # commit changes
    conn.commit()
    
    # close the connection
    conn.close()

"""
Function that saves user allergen data to the database.
If they are already in the database, updates the information.
"""
def save_user_allergens(user_id, username, selected_allergens):
    # create or connect to our database
    conn = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursor = conn.cursor()

    # find the table name according to the location name, makes it safe for table names as well
    table_name = "user_data"

    # set all to 0 for now assuming they have no allergies
    allergyDairy = 0
    allergyEgg = 0
    allergyFish = 0
    allergyPeanuts = 0
    allergyShellfish = 0
    allergySoy = 0
    allergySesame = 0
    allergyTreeNuts = 0
    allergyWheatGluten = 0

    # below lines work on the incoming selected locations array, check each possible input to see what they selected
    if "dairy" in selected_allergens:
        allergyDairy = 1
    if "egg" in selected_allergens:
        allergyEgg = 1
    if "fish" in selected_allergens:
        allergyFish = 1
    if "peanuts" in selected_allergens:
        allergyPeanuts = 1
    if "shellfish" in selected_allergens:
        allergyShellfish = 1
    if "soy" in selected_allergens:
        allergySoy = 1
    if "sesame_tahini" in selected_allergens:
        allergySesame = 1
    if "wheat_gluten" in selected_allergens:
        allergyWheatGluten = 1
    if "tree_nuts" in selected_allergens:
        allergyTreeNuts = 1


    # create new table if it doesn't exist (shouldn't happen more than once)
    cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        user_id TEXT PRIMARY KEY,
                        username TEXT,
                        frileySelect INTEGER CHECK (frileySelect IN (0,1)),
                        seasonsSelect INTEGER CHECK (seasonsSelect IN (0,1)),
                        unionSelect INTEGER CHECK (unionSelect IN (0,1)),
                        halalDiet INTEGER CHECK (halalDiet IN (0,1)),
                        veganDiet INTEGER CHECK (veganDiet IN (0,1)),
                        vegetarianDiet INTEGER CHECK (vegetarianDiet IN (0,1)),
                        allergicDairy INTEGER CHECK (allergicDairy IN (0,1)),
                        allergicEggs INTEGER CHECK (allergicEggs IN (0,1)),
                        allergicFish INTEGER CHECK (allergicFish IN (0,1)),
                        allergicPeanuts INTEGER CHECK (allergicPeanuts IN (0,1)),
                        allergicShellfish INTEGER CHECK (allergicShellfish IN (0,1)),
                        allergicSoy INTEGER CHECK (allergicSoy IN (0,1)),
                        allergicSesame INTEGER CHECK (allergicSesame IN (0,1)),
                        allergicTreeNuts INTEGER CHECK (allergicTreeNuts IN (0,1)),
                        allergicWheatGluten INTEGER CHECK (allergicWheatGluten IN (0,1))
                    )
                    """)
    
    # insert new person or update person if the user_id is already in the table
    cursor.execute(f"""
                    INSERT INTO {table_name} (user_id, username, frileySelect, seasonsSelect, unionSelect,
                                              halalDiet, veganDiet, vegetarianDiet,
                                              allergicDairy, allergicEggs, allergicFish, allergicPeanuts,
                                              allergicShellfish, allergicSoy, allergicSesame, allergicTreeNuts, allergicWheatGluten) 
                    VALUES (?, ?, ?, ?, ?,
                            ?, ?, ?,
                            ?, ?, ?, ?,
                            ?, ?, ?, ?, ?) 
                    ON CONFLICT (user_id) DO UPDATE SET 
                    username = excluded.username,
                    allergicDairy = excluded.allergicDairy,
                    allergicEggs = excluded.allergicEggs,
                    allergicFish = excluded.allergicFish,
                    allergicPeanuts = excluded.allergicPeanuts,
                    allergicShellfish = excluded.allergicShellfish,
                    allergicSoy = excluded.allergicSoy,
                    allergicSesame = excluded.allergicSesame,
                    allergicTreeNuts = excluded.allergicTreeNuts,
                    allergicWheatGluten = excluded.allergicWheatGluten
                    """, 
                    (user_id, username, 0, 0, 0,
                     0, 0, 0,
                     allergyDairy, allergyEgg, allergyFish, allergyPeanuts,
                     allergyShellfish, allergySoy, allergySesame, allergyTreeNuts, allergyWheatGluten))
    
    # commit changes
    conn.commit()
    
    # close the connection
    conn.close()

"""
Find starting location for the paginator depending on the person who requested.
"""
# SELECT item_name FROM menu_items WHERE
def findFirstPlace(user_id):

    # create or connect to our database
    connUser = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursorUser = connUser.cursor()

    # create or connect to our other database
    connDining = sqlite3.connect("DiningHalls.db")

    # the cursor allows us to use sql commands
    cursorDining = connDining.cursor()

    table_name = "user_data"

    cursorUser.execute(f"""
                       SELECT *
                       FROM {table_name}
                       WHERE user_id = {user_id}
                       """)
    
    specificPersonList = cursorUser.fetchall()

    print(specificPersonList)

    firstPlace = ""

    if specificPersonList[0][2] == 1:
        firstPlace = "Friley"
    elif specificPersonList[0][3] == 1:
        firstPlace = "Seasons"
    elif specificPersonList[0][4] == 1:
        firstPlace = "Union"

    print(firstPlace)

    return firstPlace

"""
Fetch all of the data for a specific user. Works for intro & furthermore.
"""
# SELECT item_name FROM menu_items WHERE
def findData_forUser(user_id, username, location, time):

    # create or connect to our database
    connUser = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursorUser = connUser.cursor()

    # create or connect to our other database
    connDining = sqlite3.connect("DiningHalls.db")

    # the cursor allows us to use sql commands
    cursorDining = connDining.cursor()

    table_name = "user_data"

    cursorUser.execute(f"""
                       SELECT *
                       FROM {table_name}
                       WHERE user_id = {user_id}
                       """)
    
    specificPersonList = cursorUser.fetchall()

    print(specificPersonList)

    firstPlace = specificPersonList[0][3]

    print(firstPlace)


