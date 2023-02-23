import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import pymysql
import os
from pprint import pprint
import simplejson as json
import requests
import time
from IPython.display import display

HOST = "dbikes.cs7qau9ecvp4.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "admin"
PASSWORD = "group8ucd"

# engine is a complex software that takes input from python app and processes the information and converts into out that sql data
# base can understand

# checking pymysql connection
# pymysql.connect(host="dbikes.cs7qau9ecvp4.us-east-1.rds.amazonaws.com",
#                 user="admin",
#                 password="group8ucd",
#                 database="dbbikes",
#                 charset="utf8mb4",
#                 cursorclass=pymysql.cursors.DictCursor)


engine = create_engine(
    "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, HOST, PORT, DB), echo=True)

# creating database
sql = """
CREATE DATABASE IF NOT EXISTS dbbikes;
"""
engine.execute(sql)


for res in engine.execute("SHOW VARIABLES;"):
    print(res)
