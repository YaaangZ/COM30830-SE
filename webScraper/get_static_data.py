import sqlalchemy as sqla
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import traceback
import glob
import json
import requests
import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import MySQL, APIkeys


# engine is a complex software that takes input from python app and processes the information and converts into out that sql data
# base can understand


def get_engine():
    engine = create_engine(MySQL.URI, echo=True)
    return engine

# checking my connection

def check_connection():
    engine = get_engine()
    with engine.connect() as conn:
        for res in conn.execute(text("SHOW VARIABLES")):
            print(res)

check_connection()


def create_dbbikes_database():
    engine = get_engine()

# creating database

    sql1 = '''
    CREATE DATABASE IF NOT EXISTS dbbikes;
    '''

    # creating a table for station
    sql2 = '''
    DROP TABLE IF EXISTS station;
    '''

    sql3 = '''
    CREATE TABLE station(number integer not null, name varchar(128), address varchar(128), position_lat decimal(8,6), position_lng decimal(9,6), banking integer, bonus integer, bike_stands integer, primary key(number),unique(name));
    '''


    # drop table if exists
    sql4 = ''' DROP TABLE IF EXISTS availability'''

    # creating a table for availability

    sql5 = '''
    CREATE TABLE availability(number integer not null, available_bike_stands integer, available_bikes integer, status varchar(128), last_update integer, primary key(number, last_update));
    '''
    with engine.connect() as conn:
        conn.begin()
        try:
            conn.execute(sql1)
            conn.execute(sql2)
            conn.execute(sql3)
            conn.execute(sql4)
            conn.execute(sql5)
            conn.commit()
        except Exception as e:
            traceback.format_exc()

create_dbbikes_database()

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

    with engine.connect() as conn:
        conn.begin()
        try:
            for station in station:
                row = (station.get("number"), station.get("name"), station.get("address"), station.get("position").get("lat"), station.get(
                        "position").get("lng"), int(station.get("banking")), int(station.get("bonus")), station.get("bike_stands"))
               
                conn.execute(store_station_sql, row) 
            conn.commit()
        except Exception as e:
            traceback.format_exc()

store_station_information()

# function to store availability data into availablity table


def store_availability_information():
    station_availability = get_dbData()
    engine = get_engine()
    store_availability_sql = "insert into availability values(%s, %s, %s, %s, %s)"
    with engine.connect() as conn:
        conn.begin()

        for station in station_availability:
            row = (station.get("number"), station.get("available_bike_stands"),
                station.get("available_bikes"), station.get("status"), station.get("last_update")//1000)
                # print(row)
            try:
                conn.execute(store_availability_sql, row)
                conn.commit()
            except IntegrityError:
                continue
            except Exception as e:
                traceback.format_exc()

        

store_availability_information()
