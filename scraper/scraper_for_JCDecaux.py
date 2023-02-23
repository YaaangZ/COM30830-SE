import requests
import json
from dbinfo import *
import traceback
import time


def main():
    # use Crontab to execute every 5 mins
    while True:
        try:
            r = requests.get(STATIONS_URI, params={"contract": NAME,
                                                   "apiKey": APIKEY})
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
