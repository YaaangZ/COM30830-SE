import json

from flask import jsonify, render_template
from app import db
from app import app
from services import StationService, AvailabilityService

station_service = StationService(db)
availability_service = AvailabilityService(db)


@app.route('/station/<int:number>', methods=['GET'])
def get_station(number):
    station = station_service.get_station_by_number(number)
    if station:
        # return station.to_dict()
        return jsonify(station.to_dict())
    else:
        return jsonify({'error': 'Station not found'}), 404

@app.route('/stations')
def get_all_station():
    stations = station_service.get_all_stations()
    serialized_stations = [s.to_dict() for s in stations]
    return jsonify(serialized_stations)
@app.route('/availability/<int:number>', methods=['GET'])
def get_avalability(number):
    availability = availability_service.get_availability_by_number(number)
    if availability is not None:
        return jsonify(availability.to_dir())
    else:
        return jsonify({'error': 'Availability not found'}), 404
@app.route('/map')
def map():
    # animal = "Yun"
    # return render_template("home.html", animal_flask=animal)
    return render_template("home.html")
    # return render_template("new.html")
if __name__ == '__main__':
    app.run(debug=True)