import json

from flask import jsonify
from app import db
from app import app
from services import StationService

station_service = StationService(db)


@app.route('/station/<int:number>', methods=['GET'])
def get_station(number):
    station = station_service.get_station_by_number(number)
    if station:
        # return station.to_dict()
        return jsonify(station.to_dict())
    else:
        return jsonify({'error': 'Station not found'}), 404

@app.route('/station')
def get_all_station():
    stations = station_service.get_all_stations()
    stations_json = json.dumps(stations)
    return jsonify(stations_json)

@app.route('/hello')
def hello():
    return jsonify({'haha': 'you see'})

if __name__ == '__main__':
    app.run(debug=True)