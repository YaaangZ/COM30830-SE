import sys
import os
import pymysql


# bike api
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
NAME = "Dublin"


class APIkeys:
    Bike_APIKEY = "92a580e0a48e1f31ade6e2c8c40372a25f10c56e"
    weather_APIKEY = "86c4b57818061dc4cebb5e6a32d09692"


# sql information

class MySQL:
    HOST = "dbikes.cs7qau9ecvp4.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    DB = "dbbikes"
    USER = "admin"
    PASSWORD = "group8ucd"
    URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'