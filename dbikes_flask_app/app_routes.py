from flask import Flask, render_template, jsonify, request, url_for
from flask_caching import Cache
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import traceback
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config_info.config_info import MySQL, APIkeys
from webScraper.weather_forcast_data import scrap_weather
from webScraper.get_static_data import get_engine
# creates flask app 
app = Flask(__name__, static_url_path='/static')
# connect app caching 

app.config['SQLALCHEMY_DATABASE_URI'] = MySQL.URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)


# route1: homeage 
@app.route('/')
# @cache.cached()
def index():
    map_api = APIkeys.map_APIKEY
    return render_template("index.html", map_apikey=map_api)

# # route2: getting all sations 
@app.route("/stations")
# @cache.cached()
def get_all_station():
    '''Return a list of all the stations'''
    engine = get_engine();
    sql = """SELECT s.number, s.name, s.address, s.position_lat, s.position_lng,
               a.available_bike_stands, a.available_bikes,
               a.status, a.last_update
            FROM station s
            LEFT JOIN availability a ON s.number = a.number
            WHERE a.last_update = (
            SELECT MAX(last_update) 
            FROM availability
            WHERE number = s.number
        )
        ORDER BY s.number;"""
    try: 
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            return jsonify([row._asdict() for row in rows])
    except Exception as e:
        print(traceback.format_exc())
    

# # route3: getting specific station by id 
@app.route('/stations/<int:station_id>')
# @cache.cached()
def get_station(station_id):
    engine = get_engine()
    sql = f"""           SELECT s.number, s.name, s.address, s.position_lat, s.position_lng, 
              a.available_bike_stands, a.available_bikes, 
              a.status, a.last_update 
        FROM station s 
        LEFT JOIN availability a ON s.number = a.number 
        WHERE s.number = {station_id} AND a.last_update = ( 
            SELECT MAX(last_update) 
            FROM availability 
            WHERE number = s.number 
        )"""
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            return jsonify([row._asdict() for row in rows])
    except Exception as e:
        print(traceback.format_exc())

# # route4: weather information 
# @app.route('/weather/')
# # @cache.cached(timeout= 300)

# def get_weather(station_id):
#     '''Return current weather oinformation'''

# # route5: function to return hourly availability 


# # route6: function to return daily availablity 
# @app.route('/contact')
# @cache.cached()
# def contact():
#     return render_template('contact.html')


# route 6 

# app.route("/occupancy/<int:station_id>")
if __name__ == "__main__":
    app.run(debug=True)