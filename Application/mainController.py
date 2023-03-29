import traceback

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
# @functools.lru_cache(maxsize=128)
def get_stations():
    engine = get_engine()
    sql = "select * from station;"
    try:
        with engine.connect() as conn:
            rows = conn.execute(text(sql)).fetchall()
            print('#found {} stations', len(rows), rows)
        return jsonify([row._asdict() for row in rows])  # use this formula to turn the rows into a list of dicts
        # return render_template("index.html", apikey=config.APIKEY)
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404


@app.route("/occupancy/<int:station_id>")
def get_occupancy():
    return render_template("occupancy.html", apikey=config.APIKEY)


@app.route("/stations/<int:station_id>")
def get_station_by_id():
    return render_template("stations.html", apikey=config.APIKEY)


if __name__ == '__main__':
    app.run(debug=True)
