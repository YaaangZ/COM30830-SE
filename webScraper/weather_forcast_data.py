import requests
from sqlalchemy import create_engine, text
import datetime
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
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
    with engine.connect() as conn:
        for res in conn.execute(text("SHOW VARIABLES")):
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
            weatherMain varchar(128),
            temperature decimal(9, 6),
            feels_like decimal(9, 6),
            temp_min decimal(9, 6),
            temp_max decimal(9, 6),
            humidity decimal(9,6),
            visibility integer,
            wind_speed decimal(9, 6),
            wind_degree decimal(9, 6),
            sunrise decimal(9, 6),
            sunset decimal(9, 6),
            icon varchar(128),
            primary key(date_time)
        );'''


    with engine.connect() as conn:
        conn.begin()
        try:
            conn.execute(text(sql1))
            conn.execute(text("USE dbbikes;"))

            conn.execute(text(sql2))
            conn.execute(text(sql3))
            conn.commit()
        except Exception as e:
            print(traceback.format_exc())


create_weather_database()


def store_weatherInformation():
    Weather = scrap_weather(53.332383, -6.252717)
    engine = get_engine()
    with engine.connect() as conn:
        store_weatherInfo_sql = text("insert into weatherInformation values(:date_time,:weather_id,:weatherMain,:temperature,:feels_like,:temp_min,:temp_max,:humidity,:visibility,:wind_speed,:wind_degree,:sunrise,:sunset, :icon)")
        # main_info = json.dumps(dublin_weather['main'])
        
    
        row = {"date_time": Weather["dt"], "weather_id": Weather["weather"][0]["id"],
                       "weatherMain": Weather["weather"][0]["main"],
                       "temperature": Weather["main"]["temp"],
                       "feels_like": Weather["main"]["feels_like"],
                       "temp_min": Weather["main"]["temp_min"], "temp_max": Weather["main"]["temp_max"],
                       "humidity": Weather["main"]["humidity"], "visibility": Weather["visibility"],
                       "wind_speed": Weather["wind"]["speed"], "wind_degree": Weather["wind"]["deg"],
                       "sunrise": Weather["sys"]["sunrise"], "sunset": Weather["sys"]["sunset"], "icon": Weather['weather'][0]['icon']}
        try:
            conn.execute(store_weatherInfo_sql, row)
            conn.commit()
        except IntegrityError:
            pass
        except Exception as e:
            print(traceback.format_exc())
store_weatherInformation()
