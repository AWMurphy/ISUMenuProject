import time
from datetime import datetime

target_hour = 2
target_minute = 19

while True:
    now = datetime.now()
    print(now)
    if now.hour == target_hour and now.minute == target_minute:
        print("It's 2:19!")
        break  # Exit the loop once the time matches
    time.sleep(30)  # Sleep for 30 seconds to avoid excessive printing