import json

from flask import jsonify, render_template
from app import db
from app import app
from services import DatbaseService

datbaseService = DatbaseService(db)


@app.route('/station/<int:number>', methods=['GET'])
def get_station(number):
    station = datbaseService.get_latest_station(number)
    if station:
        return jsonify(station)
    else:
        return jsonify({'error': 'Station not found'}), 404
@app.route('/stations')
def get_all_stations():
    stations = datbaseService.get_lastest_stations()
    return jsonify(stations)
@app.route('/occupancy/<int:number>', methods=['GET'])
def get_occupancy_24h(number):
    data_24h = datbaseService.get_occupancy_by_number_24h(number)
    serialized_data_24h = [
        {"time": row[0], "bikes": row[1], "stands": row[2]} for row in data_24h
    ]
    return jsonify(serialized_data_24h)
@app.route('/map')
def map():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)