import sys
import os
import pymysql


# bike api
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
NAME = "Dublin"


class APIkeys:
    Bike_APIKEY = "daf662cdfe4e13af1adb983d5abdfc214e3c8a0e"
    weather_APIKEY = "86c4b57818061dc4cebb5e6a32d09692"
    map_APIKEY = "AIzaSyAvFe6i9P5wR5qDTU5S_CSdIzAonznhh0Y"


# sql information

class MySQL:
    HOST = "dbikes.cs7qau9ecvp4.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    DB = "dbbikes"
    USER = "admin"
    PASSWORD = "group8ucd"
    URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB}'

