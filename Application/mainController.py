import json
import traceback
import pandas as pd

from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, text
from get_station_config_info import *

import config

app = Flask(__name__, static_url_path="/")


def get_engine():
    """
    get engine to handle database
    :return: sqlalchemy engine
    """
    engine = create_engine('mysql://{}:{}@{}/{}'.format(USER, PASSWORD, HOST, DATABASE), echo=True)
    return engine


@app.route("/")
def main():
    return render_template("index.html", apikey=config.APIKEY)


@app.route("/stations")
def get_stations():
    engine = get_engine()
    sql = "select * from station;"
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            print('#found {} stations', len(rows), rows)
        return jsonify([row._asdict() for row in rows])  # use this formula to turn the rows into a list of dicts
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404


@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    try:
        engine = get_engine()
        df = pd.read_sql_query("select * from availability where number = %(number)s", engine,
                               params={"number": station_id})
        df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
        df.set_index('last_update_date', inplace=True)
        res = df['available_bike_stands'].resample('1d').mean()
        # res['dt'] = df.index
        print(res)
        return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index), res.values))))
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify(error="An error occurred"), 500


@app.route("/stations/<int:station_id>")
def get_station_by_id():
    return render_template("stations.html", apikey=config.APIKEY)


if __name__ == '__main__':
    app.run(debug=True)
