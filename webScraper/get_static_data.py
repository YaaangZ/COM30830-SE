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
# ensuring my connection is being closed == this lead to 64 connections 

def get_engine():
    engine = create_engine(MySQL.URI, echo=True)
    return engine

# checking my connection

def check_connection():
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(text("show variables"))
        for row in res:
            print(row)
            break



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
            conn.execute(text(sql1))
            conn.execute(text("USE dbbikes;"))
            conn.execute(text(sql2))
            conn.execute(text(sql3))
            conn.execute(text(sql4))
            conn.execute(text(sql5))
            conn.commit()
        except Exception as e:
            print(traceback.format_exc())


# method to get the data


def get_dbData():
    STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
    NAME = "Dublin"
    try:
        r = requests.get(STATIONS_URI, params={"contract": NAME,
                                           "apiKey": APIkeys.Bike_APIKEY})
        return json.loads(r.text)
    except Exception as e:
            print(traceback.format_exc())
# function to store information into station table


def store_station_information():
    station = get_dbData()
    engine = get_engine()
    store_station_sql = text("insert into station values(:number,:name,:address,:position_lat,:position_lng,:banking,:bonus,:bike_stands)")

    with engine.connect() as conn:
        conn.begin()
        try:
            for station in station:
                row = {"number": station.get("number"), "name": station.get("name"),
                               "address": station.get("address"),
                               "position_lat": station.get("position").get("lat"),
                               "position_lng": station.get("position").get("lng"),
                               "banking": int(station.get("banking")), "bonus": int(station.get("bonus")),
                               "bike_stands": station.get("bike_stands")}
                conn.execute(store_station_sql, row)
            conn.commit()
        except Exception as e:
            print(traceback.format_exc())

# function to store availability data into availablity table

# takes logger as an input 
def store_availability_information(logger):
    station_availability = get_dbData()
    engine = get_engine()
    number_of_updates = 0   #check number of updates 
    store_availability_sql = text("insert into availability values(:number,:available_bike_stands,:available_bikes,:status,:last_update)")

    with engine.connect() as conn:
        for station in station_availability:
            row = {"number": station.get("number"),
                           "available_bike_stands": station.get("available_bike_stands"),
                           "available_bikes": station.get("available_bikes"), "status": station.get("status"),
                           "last_update": station.get("last_update") // 1000}

                # print(row)
            try:
                conn.execute(store_availability_sql, row)
                conn.commit()
                number_of_updates +=1 
            except IntegrityError:
                continue
            except Exception as e:
                print(traceback.format_exc())           
    return number_of_updates  #return number of updates 
