import json

from flask import jsonify, render_template, request
from app import db
from app import app
from services import DatbaseService, ModelService, RecommendService
from datetime import datetime
datbaseService = DatbaseService(db)
modelService = ModelService()
# recommendService = RecommendService()
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

# @app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict():
    # input_data = request.json
    # just test data
    input_data = {
        'time': datetime.now(),
        'number': 42
    }

    station = datbaseService.get_station_static(input_data["number"])
    result = modelService.predict(station, input_data["time"])

    return result
@app.route('/predict_5d/<int:number>', methods=['GET'])
def predict_5d(number):
    station = datbaseService.get_station_static(number)

    result = modelService.predict_5d(station)

    return result
@app.route('/predict_24h/<int:number>', methods=['GET'])
def predict_24h(number):
    station = datbaseService.get_station_static(number)

    result = modelService.predict_24h(station)
    return result
@app.route('/plan', methods=['GET'])
def plan():
    # a = request
    # test_data = {
    # }
    location = (53.350140, -6.266155)
    RecommendService.recommend(location, 1)
    return "test"
@app.route('/map')
def map():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)