import requests
import json
from config_info.config import APIkeys
import traceback
import time


def main():
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    NAME = "Dublin"

    # use Crontab to execute every 5 mins
    while True:
        try:
            r = requests.get(STATIONS_URI, params={"contract": NAME,
                                                   "apiKey": APIkeys.Bike_APIKEY})
            # change to python object
            station_info_obj = json.loads(r.text)
            # store(station_info_obj)
            # store the data (db and/or text files)
            print(station_info_obj)
            # time.sleep(5*60)
        except:
            # if there is any problem, print the traceback
            print(traceback.format_exc())

    return


main()
