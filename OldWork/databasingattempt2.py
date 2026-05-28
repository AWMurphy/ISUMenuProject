import sqlite3
from OldWork.calories import PrintMenus

# more setup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

def dataBasing():
    #setting shit up
    driver = webdriver.Edge()

    # Connect to SQLite (or create the database file)
    conn = sqlite3.connect('fooditems.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()


    # Create a table
    cursor.execute('''
    CREATE TABLE foods (
        item_name TEXT PRIMARY KEY,
        calories TEXT NOT NULL,
        categories TEXT
    )'''
    )


    namesList, caloriesList, categoriesList = PrintMenus(driver, "https://www.dining.iastate.edu/location/friley-windows-2-2")

    for i in range(len(namesList)):
        # Insert data into the table
        cursor.execute('''
        INSERT INTO foods (item_name, calories) 
        VALUES (?, ?)
        ''', (namesList[i], caloriesList[i]))

    for i in range(len(namesList)):
        newCatList = []
        newCatList = categoriesList[i]
        if newCatList == []:
            newCatList = ['Categories: Not Available']

        for j in range(len(newCatList)):
        # Concatenate the new category value with a comma only if categories already exists
        # TRY AND FIX THE FIRST FUCKING WHEN CASE IT DOESNT FUCKING GODDAMN WORK
            cursor.execute('''
            UPDATE foods
            SET categories = 
                CASE  
                    WHEN categories IS NULL THEN ?  
                    WHEN categories = '' THEN ?    
                    ELSE categories || ', ' || ? 
                END
            WHERE item_name = ?
            ''', (newCatList[j], newCatList[j], newCatList[j], namesList[i]))

    # just for now
    #cursor.execute('''
    #        DELETE FROM foods
    #        WHERE categories LIKE '%Category: Vegan%'
    #        ''')


    # Commit the changes and close the connection
    conn.commit()
    #conn.close()

    print("Database and table created successfully!")

    # list of things to get done
    # > 1 - try and fix any bugs with current code
    # > 2 - possible figure out how to manage tables so that it doesn't error everytime i don't delete it
    # > 3 - merge tables so we can add new products without tables duplicating or breaking
    # > 4 - try discord bot integration

    cursor.execute("SELECT * FROM foods")

    rows = cursor.fetchall()

    print(rows)

    # Print the fetched rows
    for row in rows:
        print(row)

    print("this is printing")

    conn.close()

    return rows
