import json

from flask import jsonify, render_template, request
from . import db, GoogleMap_API_KEY
# from app import db, GoogleMap_API_KEY
# from app import app
from . import app
from .services import DatbaseService, ModelService, RecommendService
from datetime import datetime
datbaseService = DatbaseService(db)
modelService = ModelService()
recommendService = RecommendService(modelService)

@app.route('/station/<int:number>', methods=['GET'])
def get_station(number):
    print("Registering get_station")
    station = datbaseService.get_latest_station(number)
    if station:
        return jsonify(station)
    else:
        return jsonify({'error': 'Station not found'}), 404
@app.route('/stations')
def get_all_stations():
    print("Registering get_all_stations")
    stations = datbaseService.get_lastest_stations()
    return jsonify(stations)
@app.route('/occupancy/<int:number>', methods=['GET'])
def get_occupancy_24h(number):
    print("Registering get_occupancy_24h")
    data_24h = datbaseService.get_occupancy_by_number_24h(number)
    serialized_data_24h = [
        {"time": row[0], "bikes": row[1], "stands": row[2]} for row in data_24h
    ]
    return jsonify(serialized_data_24h)
# @app.route('/predict', methods=['POST'])
# def predict():
#     print("Registering predict")
#     # input_data = request.json
#     # just test data
#     input_data = {
#         'time': datetime.now(),
#         'number': 42
#     }
#
#     station = datbaseService.get_station_static(input_data["number"])
#     result = modelService.predict(station, input_data["time"])
#
#     return result
@app.route('/predict_5d/<int:number>', methods=['GET'])
def predict_5d(number):
    print("Registering predict_5d")
    station = datbaseService.get_station_static(number)

    result = modelService.predict_5d(station)

    return result
@app.route('/predict_24h/<int:number>', methods=['GET'])
def predict_24h(number):
    print("Registering predict_24h")
    station = datbaseService.get_station_static(number)

    result = modelService.predict_24h(station)
    return result
@app.route('/plan', methods=['POST'])
def plan():
    print("Registering plan")

    journey_date = request.form.get('journeydate')
    journey_time = request.form.get('journeytime')
    journey_from = request.form.get('journeyfrom')
    journey_to = request.form.get('journeyto')
    journey_mode = request.form.get('type')

    if journey_date == "":
        date_obj = datetime.now().date()
    else:
        date_obj = datetime.strptime(journey_date, "%Y-%m-%d").date()
    if journey_time == "":
        time_obj = datetime.now().time()
    else:
        time_obj = datetime.strptime(journey_time, "%H:%M").time()

    datetime_obj = datetime.combine(date_obj, time_obj)

    origin_lat_lng = request.form.get('origin_lat_lng')
    destination_lat_lng = request.form.get('destination_lat_lng')

    if origin_lat_lng and destination_lat_lng:
        origin_lat, origin_lng = map(float, origin_lat_lng.split(','))
        destination_lat, destination_lng = map(float, destination_lat_lng.split(','))
        orig = recommendService.recommend((origin_lat, origin_lng), datetime_obj, "orig")
        des = recommendService.recommend((destination_lat, destination_lng), datetime_obj, "des")
        result = {"orig": orig, "des": des}
        return result
        # test data
        # return jsonify({
        #     "orig": {"number": 42, "bikes": 10},
        #     "des": {"number": 43, "stands": 12}
        # })
        # RecommendService.recommend()
    else:
        return jsonify({"error": "Missing origin or destination coordinates."})
@app.route('/')
def index():
    print("Registering index")
    # myKEY = GoogleMap_API_KEY
    return render_template("home.html", googleKey=GoogleMap_API_KEY)
if __name__ == '__main__':
    app.run(debug=True)