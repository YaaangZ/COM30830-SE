import json
import traceback

import requests
from sqlalchemy import create_engine, text

from weatherInfo.config_info import *


def get_engine():
    """
    get engine to handle database
    :return: sqlalchemy engine
    """
    engine = create_engine('mysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE), echo=True)
    return engine


def get_data():
    """
    scraping data from OpenWeather
    :return: JSON
    """
    r = requests.get(CUrWeatherURI)
    # change response json to python object
    return json.loads(r.text)


def init_database():
    """
    Initialize database
    :return: None
    """
    engine = get_engine()
    sql1 = "create database if not exists dbbikes;"
    sql2 = """
    use dbbikes;
    drop table if exists tb_weather;
    create table tb_weather(
        `updatedTime` integer not null,
        `weatherId` integer not null,
        `weatherMain` varchar(128),
        `temp` float,
        feels_like float,
        temp_min float,
        temp_max float,
        humidity float,
        visibility integer,
        windSpeed float,
        windDeg float,
        sunrise integer,
        sunset integer,
        primary key(`updatedTime`)
    );
    """

    with engine.connect() as conn:
        conn.begin()
        try:
            conn.execute(text(sql1))
            conn.execute(text(sql2))
            conn.commit()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"An error occurred: {e}\n{tb}")


def store_weather_data():
    """
    store weather in the tb_weather
    :return: None
    """
    Weather = get_data()
    engine = get_engine()
    with engine.connect() as conn:
        pre_sql = text(
            "insert into tb_weather values(:updatedTime,:weatherId,:weatherMain,:temp,:feels_like,:temp_min,:temp_max,:humidity,:visibility,:windSpeed,:windDeg,:sunrise,:sunset)")
        conn.begin()
        try:
            # for weather in Weather:
            insert_data = {"updatedTime": Weather["dt"], "weatherId": Weather["weather"][0]["id"],
                           "weatherMain": Weather["weather"][0]["main"],
                           "temp": Weather["main"]["temp"],
                           "feels_like": Weather["main"]["feels_like"],
                           "temp_min": Weather["main"]["temp_min"], "temp_max": Weather["main"]["temp_max"],
                           "humidity": Weather["main"]["humidity"], "visibility": Weather["visibility"],
                           "windSpeed": Weather["wind"]["speed"], "windDeg": Weather["wind"]["deg"],
                           "sunrise": Weather["sys"]["sunrise"], "sunset": Weather["sys"]["sunset"]}

            conn.execute(pre_sql, insert_data)
            conn.commit()
        except Exception as e:
            tb = traceback.format_exc()
            print(f"An error occurred: {e}\n{tb}")


def crawl():
    """

    :return:
    """
    # use Crontab to execute every 5 mins
    try:
        store_availability()
    except Exception as e:
        # if there is any problem, print the traceback
        # use logging or something?
        print(traceback.format_exc())
