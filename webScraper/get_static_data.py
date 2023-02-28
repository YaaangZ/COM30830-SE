from config_info.config_info import MySQL, APIkeys
import time
import requests
import json
import glob
import traceback
from sqlalchemy import create_engine
import sqlalchemy as sqla
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


# engine is a complex software that takes input from python app and processes the information and converts into out that sql data
# base can understand


def get_engine():
    engine = create_engine(MySQL.URI, echo=True)
    return engine

# checking my connection


def check_connection():
    engine = get_engine()

    for res in engine.execute("SHOW VARIABLES"):
        print(res)


check_connection()


def create_dbbikes_database():
    engine = get_engine()

    # creating database

    sql1 = """
    CREATE DATABASE IF NOT EXISTS dbbikes;
    """

    # creating a table for station

    sql2 = """
    DROP TABLE IF EXISTS station;
    CREATE TABLE IF NOT EXISTS station(
        number integer not null, 
        name varchar(128), 
        address varchar(128), 
        position_lat decimal(8,6), 
        position_lng decimal(9,6), 
        banking integer, 
        bonus integer,
        bike_stands integer, 
        primary key(number), 
        unique(name)
    );
    """

    # creating a table for availability

    sql3 = """
    DROP TABLE IF EXISTS availability;
    CREATE TABLE IF NOT EXISTS availability(
        number integer not null,
        available_bike_stands integer,
        available_bikes integer,
        status varchar(128),
        last_update integer,
        primary key(number, last_update)
    );
    """

    engine.execute(sql1)
    engine.execute(sql2)
    engine.execute(sql3)

# create_dbbikes_database()

# method to get the data


def get_dbData():
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    NAME = "Dublin"

    r = requests.get(STATIONS_URI, params={"contract": NAME,
                                           "apiKey": APIkeys.Bike_APIKEY})
    return json.loads(r.text)

# function to store information into station table


def store_station_information():

    station = get_dbData()
    engine = get_engine()
    store_station_sql = "insert into station values(%s, %s, %s, %s, %s, %s, %s, %s)"

    for station in station:
        row = (station.get("number"), station.get("name"), station.get("address"), station.get("position").get("lat"), station.get(
            "position").get("lng"), int(station.get("banking")), int(station.get("bonus")), station.get("bike_stands"))

        engine.execute(store_station_sql, row)


# store_station_information()

# function to store availability data into availablity table


def store_availability_information():
    station_availability = get_dbData()
    engine = get_engine()
    store_availability_sql = "insert into availability values(%s, %s, %s, %s, %s)"

    for station in station_availability:
        row = (station.get("number"), station.get("available_bike_stands"),
               station.get("available_bikes"), station.get("status"), station.get("last_update")//1000)
        # print(row)
        engine.execute(store_availability_sql, row)


store_availability_information()
