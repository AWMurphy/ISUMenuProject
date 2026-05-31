import sqlite3

def save_to_database_per_location(appropriate_data, location_name):
    """
    Saves the json/dictionary into a table named after the dining hall in DiningHalls.db
    """

    # create or connect to our database
    conn = sqlite3.connect("DiningHalls.db")

    # the cursor allows us to use sql commands
    cursor = conn.cursor()

    # find the table name according to the location name, makes it safe for table names as well
    table_name = location_name.replace(" ", "_").lower()

    # wipe old table data so we can create a new table for it < if the table is created
    cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")

    # create new table freshly
    cursor.execute(f"""
                    CREATE TABLE {table_name} (
                        item_id TEXT PRIMARY KEY,
                        name TEXT,
                        calories INTEGER,
                        calorieError INTEGER CHECK (calorieError IN (0,1)),
                        timeOfDay TEXT,
                        venue TEXT,
                        station TEXT,
                        category TEXT,
                        isHalal INTEGER CHECK (isHalal IN (0,1)),
                        isVegan INTEGER CHECK (isVegan IN (0,1)),
                        isVegetarian INTEGER CHECK (isVegetarian IN (0,1)),
                        containsDairy INTEGER CHECK (containsDairy IN (0,1)),
                        containsEggs INTEGER CHECK (containsEggs IN (0,1)),
                        containsFish INTEGER CHECK (containsFish IN (0,1)),
                        containsPeanuts INTEGER CHECK (containsPeanuts IN (0,1)),
                        containsShellfish INTEGER CHECK (containsShellfish IN (0,1)),
                        containsSoy INTEGER CHECK (containsSoy IN (0,1)),
                        containsSesame INTEGER CHECK (containsSesame IN (0,1)),
                        containsTreeNuts INTEGER CHECK (containsTreeNuts IN (0,1)),
                        containsWheatGluten INTEGER CHECK (containsWheatGluten IN (0,1))
                    )
                    """)
    
    # take our data from the json and put it into our database
    for item_id, details in appropriate_data.items():
        cursor.execute(f"""INSERT INTO {table_name}
                       (item_id, name, calories, calorieError, timeOfDay, venue, station, category,
                       isHalal, isVegan, isVegetarian,
                       containsDairy, containsEggs, containsFish, containsPeanuts,
                       containsShellfish, containsSoy, containsSesame, containsTreeNuts,
                       containsWheatGluten)
                       VALUES
                       (?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?,
                        ?, ?, ?, ?,
                        ?, ?, ?, ?,
                        ?)
                       """,
                       (item_id, details["name"], details["calories"], details["calorieError"], details["time_of_day"], details["venue"], details["station"], details["category"],
                        details["isHalal"], details["isVegan"], details["isVegetarian"],
                        details["containsDairy"], details["containsEggs"], details["containsFish"], details["containsPeanuts"],
                        details["containsShellfish"], details["containsSoy"], details["containsSesame"], details["containsTreeNuts"],
                        details["containsWheatGluten"]))
        
    # commit changes
    conn.commit()
    
    # close the connection
    conn.close()