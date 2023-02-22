import requests
import json
import traceback
from sqlalchemy import create_engine

from bikeInfo.config_info import *


def get_engine():
    """
    get engine to handle database
    :return: sqlalchemy engine
    """
    engine = create_engine('mysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE), echo=True)
    return engine


def check_connection():
    """
    check if engine connected to mysql server
    :return:
    """
    engine = get_engine()
    for res in engine.execute("show variables"):
        print(res)


def init_database():
    """
    create database: dbbikes
    create table: station, availability
    :return:
    """
    engine = get_engine()
    sql1 = "create database if not exists dbbikes;"
    sql2 = """
    use dbbikes;
    drop table if exists station;
    create table station(
        `number` integer not null,
        `name` varchar(128),
        address varchar(128),
        position_lat decimal(8,6),
        position_lng decimal(9,6),
        banking integer,
        bonus integer,
        bike_stands integer,
        primary key(`number`),
        unique(`name`)
    );
    """
    sql3 = """
    drop table if exists availability;
    create table availability(
        `number` integer not null,
        available_bike_stands integer,
        available_bikes integer,
        `status` varcharacter(128),
        last_update integer,
        primary key(`number`, last_update)
    );
    """
    engine.execute(sql1)
    engine.execute(sql2)
    engine.execute(sql3)


def get_data():
    """
    get data from JCDecaux API
    :return: python object of response json
    """
    r = requests.get(STATIONS_URI, params={"apiKey": JCKEY, "contract": NAME})
    # change response json to python object
    return json.loads(r.text)


def store_station():
    """
    insert static data into table 'station'
    :return:
    """
    stations = get_data()
    engine = get_engine()
    pre_sql = "insert into station values(%s,%s,%s,%s,%s,%s,%s,%s)"
    for station in stations:
        row = (station.get("number"), station.get("name"),
               station.get("address"), station.get("position").get("lat"),
               station.get("position").get("lng"), int(station.get("banking")),
               int(station.get("bonus")), station.get("bike_stands")
               )

        engine.execute(pre_sql, row)


def store_availability():
    """
    insert dynamic data into table 'availability'
    :return:
    """
    stations = get_data()
    engine = get_engine()
    pre_sql = "insert into availability values(%s,%s,%s,%s,%s)"
    for station in stations:
        row = (station.get("number"), station.get("available_bike_stands"),
               station.get("available_bikes"), station.get("status"),
               station.get("last_update")
               )
        engine.execute(pre_sql, row)


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
