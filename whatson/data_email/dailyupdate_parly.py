import sys
import subprocess
import time
from time import gmtime, strftime

while True:
    day_now = strftime("%A", time.gmtime())
    print(day_now)
    hour_now = strftime("%H", time.gmtime())
    print(hour_now)
    #if it's not a Saturday, run the programme to send the weekly or daily parly agenda update
    if day_now != "Saturday":
        if day_now == "Sunday":
            if hour_now == "15":
                subprocess.run([sys.executable, "emailwhatson.py"])
        elif hour_now == "04":
            subprocess.run([sys.executable, "emailwhatson.py"])
    #sleep for one hour and then check what time it is again
    time.sleep(3600)
