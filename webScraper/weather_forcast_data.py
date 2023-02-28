import requests
import datetime
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import MySQL, APIkeys


def scrap_weather(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APIkeys.weather_APIKEY}'
    response = requests.get(url)
    weather_data = response.json()
    return weather_data

# scrap_weather(53.33912505839768, -6.256243642329802)

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


def create_weather_database():

    engine = get_engine()

    # create database
    sql1 = """
    CREATE DATABASE IF NOT EXISTS dbbikes;
    """
    # drop table if exists
    sql2 = ''' DROP TABLE IF EXISTS weatherInformation;'''

    # creating a table for weather information

    sql3 = '''
        CREATE TABLE IF NOT EXISTS weatherInformation (
            date_time integer not null,
            weather_id integer not null,
            main varchar(128),
            description varchar(128),
            temperature decimal(9, 6),
            feels_like decimal(9, 6),
            temp_min decimal(9, 6),
            temp_max decimal(9, 6),
            visibility decimal(9, 6),
            wind_speed decimal(9, 6),
            wind_degree decimal(9, 6),
            sunrise decimal(9, 6),
            sunset decimal(9, 6),
            humidity integer,
            icon varchar(128),
            primary key(date_time)
        );'''

    sql4 = '''ALTER TABLE weatherInformation DROP COLUMN main;
    '''
    engine.execute(sql1)
    engine.execute(sql2)
    engine.execute(sql3)
    engine.execute(sql4)


# create_weather_database()


def store_weatherInformation():
    dublin_weather = scrap_weather(53.332383, -6.252717)
    engine = get_engine()
    store_weatherInfo_sql = "insert into weatherInformation values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # main_info = json.dumps(dublin_weather['main'])

    row = (dublin_weather['dt'], dublin_weather['weather'][0]['id'], dublin_weather['weather'][0]['description'], dublin_weather['main']['temp'], dublin_weather['main']['feels_like'], dublin_weather['main']['temp_min'], dublin_weather['main']
           ['temp_max'], dublin_weather['visibility'], dublin_weather['wind']['speed'], dublin_weather['wind']['deg'], dublin_weather['sys']['sunrise'], dublin_weather['sys']['sunset'], dublin_weather['main']['humidity'], dublin_weather['weather'][0]['icon'])

    engine.execute(store_weatherInfo_sql, row)


store_weatherInformation()
