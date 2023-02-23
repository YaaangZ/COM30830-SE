import requests
import json
from dbinfo import *
import traceback
import time


# from sqlalchemy import create_engine
# import pandas as pd
# # http://docs.sqlalchemy.org/en/latest/core/engines.html
# USER = "root"
# PASSWORD = "Mysqlpw1994"
# HOST = "localhost"
# DATABASE = "jdbc"
# engine = create_engine('mysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE))
#
# def store(obj):
#     # need to write.....
#     for item in obj:
#         vals = (item.get("address"), ...)
#         engine.execute("insert into dbbilke_dynamic values(%s,%s,...)", vals)
#     pass


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
            print(r.text)
            time.sleep(5*60)
        except:
            # if there is any problem, print the traceback
            print(traceback.format_exc())

    return


main()
