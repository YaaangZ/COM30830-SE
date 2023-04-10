from flask import Flask, render_template, jsonify, request, url_for
from flask_caching import Cache
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import traceback
from datetime import datetime, timedelta
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

@app.route('/occupancy/<int:station_id>')
def get_occupancy_24h(station_id):
    current_time = datetime.now()
    timestamp_24_hours_ago = datetime.timestamp(current_time - timedelta(hours=24))
    engine = get_engine()
    sql =  f"""SELECT DATE_FORMAT(FROM_UNIXTIME(availability.last_update), '%m-%d %H:00') AS hour,
       AVG(availability.available_bikes) AS avg_number_of_bikes,
       AVG(availability.available_bike_stands) AS avg_number_of_bike_stands
FROM availability
WHERE availability.number = {station_id}
AND availability.last_update >= :timestamp_24_hours_ago
GROUP BY hour
ORDER BY hour
    """
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql), {'timestamp_24_hours_ago': timestamp_24_hours_ago}).fetchall()
            serialized_data = [
            {"time": row[0], "bikes": round(row[1]), "stands": round(row[2])} for row in rows
            ]
            return jsonify(serialized_data)
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "An error occurred while processing your request."})

if __name__ == "__main__":
    app.run(debug=True)