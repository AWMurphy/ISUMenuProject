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
    if selected_locations[0] == 1:
        frileyWant = 1

    if selected_locations[1] == 1:
        seasonsWant = 1

    if selected_locations[2] == 1:
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
def isInDatabase(user_id) -> bool:

    # create or connect to our database
    conn = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursor = conn.cursor()

    # find the table name according to the location name, makes it safe for table names as well
    table_name = "user_data"

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

    # find the table name according to the diet name, makes it safe for table names as well
    table_name = "user_data"

    # set all to 0 for now assuming they want none
    halalDiet = veganDiet = vegetarianDiet = 0

    # below lines work on the incoming selected diet array, check each possible input to see what they selected
    if selected_diets[0] == 1:
        halalDiet = 1

    if selected_diets[1] == 1:
        veganDiet = 1

    if selected_diets[2] == 1:
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
    if selected_allergens[0] == 1:
        allergyDairy = 1
    if selected_allergens[1] == 1:
        allergyEgg = 1
    if selected_allergens[2] == 1:
        allergyFish = 1
    if selected_allergens[3] == 1:
        allergyPeanuts = 1
    if selected_allergens[4] == 1:
        allergyShellfish = 1
    if selected_allergens[5] == 1:
        allergySoy = 1
    if selected_allergens[6] == 1:
        allergySesame = 1
    if selected_allergens[7] == 1:
        allergyWheatGluten = 1
    if selected_allergens[8] == 1:
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

    firstPlace = ""

    locationArray = openLocations()

    print(specificPersonList)

    if specificPersonList[0][2] == 1 and locationArray[0] == 1:
        firstPlace = "Friley"
    elif specificPersonList[0][3] == 1 and locationArray[1] == 1:
        firstPlace = "Seasons"
    elif specificPersonList[0][4] == 1 and locationArray[2] == 1:
        firstPlace = "Union"

    print(firstPlace + "this")

    return firstPlace

"""
Fetch all of the data for a specific user. Works for intro & furthermore.
"""
# SELECT item_name FROM menu_items WHERE
def findData_forUser(user_id, location, time):

    # create or connect to our database
    connUser = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursorUser = connUser.cursor()

    # create or connect to our other database
    connDining = sqlite3.connect("DiningHalls.db")

    # the cursor allows us to use sql commands
    cursorDining = connDining.cursor()
    
    table_name = ""

    match location:
        case "Friley":
            table_name = "friley_windows"
        case "Seasons":
            table_name = "seasons_marketplace"
        case "Union":
            table_name = "union_drive_marketplace"

    table_names = "user_data"

    cursorUser.execute(f"""
                        SELECT *
                        FROM {table_names}
                        WHERE user_id = {user_id}
                        """)
    
    specificPersonList = cursorUser.fetchall()

    cursorDining.execute(f"""
                          PRAGMA table_info({table_name})
                          """)
    
    columnNameList = cursorDining.fetchall()

    sortingText = "" + "timeOfDay = '" + str(time).lower() + "'"

    i = 5
    j = 8
    
    while(j <= 19):

        columnName = columnNameList[j][1]

        if j < 11:
            if specificPersonList[0][i] == 1:
                sortingText = sortingText + str(f" AND {columnName} = 1")
        else:
            if specificPersonList[0][i] == 1:
                sortingText = sortingText + str(f" AND {columnName} = 0")

        i += 1
        j += 1
    
    cursorDining.execute(f"""
                          SELECT *
                          FROM {table_name}
                          WHERE {sortingText}
                          """)
    
    fullFoodList = cursorDining.fetchall()

    return fullFoodList

"""
Checks the open times for the given location.
"""
def openTimes(location):

    # create or connect to our other database
    connDining = sqlite3.connect("DiningHalls.db")

    # the cursor allows us to use sql commands
    cursorDining = connDining.cursor()

    table_name = ""

    match location:
        case "Friley":
            table_name = "friley_windows"
        case "Seasons":
            table_name = "seasons_marketplace"
        case "Union":
            table_name = "union_drive_marketplace"

    cursorDining.execute(f"""
                          SELECT *
                          FROM {table_name}
                          WHERE timeOfDay = 'breakfast'
                          """)
    
    breakfastList = cursorDining.fetchall()

    cursorDining.execute(f"""
                          SELECT *
                          FROM {table_name}
                          WHERE timeOfDay = 'lunch'
                          """)
    
    lunchList = cursorDining.fetchall()

    cursorDining.execute(f"""
                          SELECT *
                          FROM {table_name}
                          WHERE timeOfDay = 'dinner'
                          """)
    
    dinnerList = cursorDining.fetchall()

    timeList = [0] * 3
 
    if len(breakfastList) != 0:
        timeList[0] = 1
    if len(lunchList) != 0:
        timeList[1] = 1
    if len(dinnerList) != 0:
        timeList[2] = 1

    return timeList

"""
Checks the open times for the given location.
"""
def openLocations():

    # create or connect to our other database
    connDining = sqlite3.connect("DiningHalls.db")

    # the cursor allows us to use sql commands
    cursorDining = connDining.cursor()

    table_name = ""

    cursorDining.execute(f"""
                          SELECT *
                          FROM 'friley_windows'
                          """)
    
    frileyList = cursorDining.fetchall()

    cursorDining.execute(f"""
                          SELECT *
                          FROM 'seasons_marketplace'
                          """)
    
    seasonsList = cursorDining.fetchall()

    cursorDining.execute(f"""
                          SELECT *
                          FROM 'union_drive_marketplace'
                          """)
    
    unionList = cursorDining.fetchall()

    timeList = [0] * 3
 
    if len(frileyList) != 0:
        timeList[0] = 1
    if len(seasonsList) != 0:
        timeList[1] = 1
    if len(unionList) != 0:
        timeList[2] = 1

    return timeList

"""
Return list of places the user wants to see in menu.
"""
def listofPlaces(user_id) -> list:

    # create or connect to our database
    connUser = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursorUser = connUser.cursor()

    table_name = "user_data"

    cursorUser.execute(f"""
                       SELECT *
                       FROM {table_name}
                       WHERE user_id = {user_id}
                       """)
    
    specificPersonList = cursorUser.fetchall()

    output = [0] * 3
    output[0] = specificPersonList[0][2]
    output[1] = specificPersonList[0][3]
    output[2] = specificPersonList[0][4]

    return output

"""
Return list of diets the user wants to see in menu.
"""
def listofDiets(user_id) -> list:

    # create or connect to our database
    connUser = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursorUser = connUser.cursor()

    table_name = "user_data"

    cursorUser.execute(f"""
                       SELECT *
                       FROM {table_name}
                       WHERE user_id = {user_id}
                       """)
    
    specificPersonList = cursorUser.fetchall()

    output = [0] * 3
    output[0] = specificPersonList[0][5]
    output[1] = specificPersonList[0][6]
    output[2] = specificPersonList[0][7]

    return output

"""
Return list of allergens the user DOESN'T want to see in menu.
"""
def listofAllergens(user_id) -> list:

    # create or connect to our database
    connUser = sqlite3.connect("UserData.db")

    # the cursor allows us to use sql commands
    cursorUser = connUser.cursor()

    table_name = "user_data"

    cursorUser.execute(f"""
                       SELECT *
                       FROM {table_name}
                       WHERE user_id = {user_id}
                       """)
    
    specificPersonList = cursorUser.fetchall()

    output = [0] * 9
    output[0] = specificPersonList[0][8]
    output[1] = specificPersonList[0][9]
    output[2] = specificPersonList[0][10]
    output[3] = specificPersonList[0][11]
    output[4] = specificPersonList[0][12]
    output[5] = specificPersonList[0][13]
    output[6] = specificPersonList[0][14]
    output[7] = specificPersonList[0][15]
    output[8] = specificPersonList[0][16]

    return output
