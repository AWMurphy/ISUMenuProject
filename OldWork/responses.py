from random import choice, randint
import OldWork.openPlaces as openPlaces
import OldWork.databasingattempt1 as databasingattempt1

# database testing
import sqlite3

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '-openplace':
        return (str)(openPlaces.GetOpenRestaurants())
    if lowered == '-database':
        return (str)(databasingattempt1.dataBasing())
    if lowered == '-database2':
        list = databasingattempt1.dataBasing()
        return (str)(list[0])
    if lowered == 'database3':
        conn = sqlite3.connect('fooditems.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM foods")
        # finish tomorrow