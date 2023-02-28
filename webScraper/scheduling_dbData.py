import requests
import json
import traceback
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import MySQL, APIkeys

# using crontab


def main():
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    NAME = "Dublin"
    try:
        r = requests.get(STATIONS_URI, params={"contract": NAME,
                                               "apiKey": APIkeys.Bike_APIKEY})
        station_info_obj = json.loads(r.text)
    except:
        # if there is any problem, print the traceback
        print(traceback.format_exc())
    return


main()
