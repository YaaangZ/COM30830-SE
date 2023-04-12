import json
import pickle
from typing import List, Optional

import requests
from sqlalchemy import func, text

from models import Station, Availability
from datetime import datetime, timedelta
from config import weatherForecastAPI, weatherCurrentAPI, GoogleMap_API_KEY
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
class DatbaseService:
    def __init__(self, db):
        self.db = db

    def get_occupancy_by_number_24h(self, number: int):
        current_time = datetime.now()
        timestamp_24_hours_ago = datetime.timestamp(current_time - timedelta(hours=24))
        data = self.db.session.query(
                func.date_format(func.from_unixtime(Availability.last_update), "%m-%d %H:00").label('hour'),
                func.avg(Availability.available_bikes).label('avg_number_of_bikes'),
                func.avg(Availability.available_bike_stands).label('avg_number_of_bike_stands')
            ) \
            .filter(Availability.number == number) \
            .filter(Availability.last_update >= timestamp_24_hours_ago)\
            .group_by('hour') \
            .order_by('hour').all()
        processed_data = [[row[0], round(row[1]), round(row[2])] for row in data]
        return processed_data

    def get_lastest_stations(self):
        query = text("""
            SELECT s.`number`, s.`name`, s.address, s.position_lat, s.position_lng, s.banking, s.bonus, s.bike_stands, a.available_bike_stands, a.available_bikes, a.`status`, a.last_update
            FROM station s
            JOIN availability a ON s.`number` = a.`number`
            WHERE a.last_update = (
                SELECT MAX(last_update)
                FROM availability
                WHERE `number` = s.`number`
            )
            ORDER BY s.`number`;
        """)

        results = self.db.session.execute(query).fetchall()
        processed_results = []
        for row in results:
            temp_dict = dict()
            temp_dict["number"] = row[0]
            temp_dict["name"] = row[1]
            temp_dict["address"] = row[2]
            temp_dict["position_lat"] = float(row[3])
            temp_dict["position_lng"] = float(row[4])
            temp_dict["banking"] = row[5]
            temp_dict["bonus"] = row[6]
            temp_dict["bike_stands"] = row[7]
            temp_dict["available_bike_stands"] = row[8]
            temp_dict["available_bikes"] = row[9]
            temp_dict["status"] = row[10]
            temp_dict["last_update"] = row[11]
            processed_results.append(temp_dict)
        return processed_results
    def get_latest_station(self, number):
        query = text("""
            SELECT s.`number`, s.`name`, s.address, s.position_lat, s.position_lng, s.banking, s.bonus, s.bike_stands, a.available_bike_stands, a.available_bikes, a.`status`, a.last_update
            FROM station s
            JOIN availability a ON s.`number` = a.`number`
            WHERE a.last_update = (
                SELECT MAX(last_update)
                FROM availability
                WHERE `number` = s.`number`
            )
            AND s.`number` = :p_number
            ORDER BY s.`number`;
        """)

        results = self.db.session.execute(query, {"p_number": number}).fetchall()
        if len(results) == 0:
            return None
        else:
            temp_dict = dict()
            for row in results:
                temp_dict = dict()
                temp_dict["number"] = row[0]
                temp_dict["name"] = row[1]
                temp_dict["address"] = row[2]
                temp_dict["position_lat"] = float(row[3])
                temp_dict["position_lng"] = float(row[4])
                temp_dict["banking"] = row[5]
                temp_dict["bonus"] = row[6]
                temp_dict["bike_stands"] = row[7]
                temp_dict["available_bike_stands"] = row[8]
                temp_dict["available_bikes"] = row[9]
                temp_dict["status"] = row[10]
                temp_dict["last_update"] = datetime.fromtimestamp(row[11]).strftime("%b %d %H:%M:%S")

        return temp_dict
    def get_station_static(self, number):
        query = text("""
            SELECT s.*
            FROM station s
            WHERE s.`number` = :p_number;
        """)

        results = self.db.session.execute(query, {"p_number": number}).fetchall()
        if len(results) == 0:
            return None
        else:
            temp_dict = dict()
            for row in results:
                temp_dict = dict()
                temp_dict["number"] = row[0]
                temp_dict["name"] = row[1]
                temp_dict["address"] = row[2]
                temp_dict["position_lat"] = float(row[3])
                temp_dict["position_lng"] = float(row[4])
                temp_dict["banking"] = row[5]
                temp_dict["bonus"] = row[6]
                temp_dict["bike_stands"] = row[7]

        return temp_dict
    @classmethod
    def get_stations_static(cls):
        data = Station.query.all()
        processed_data = [item.to_dict() for item in data]
        return processed_data

class ModelService:
    def __init__(self):
        with open('data/random_forest_model.pkl', 'rb') as file:
            data_model = pickle.load(file)
        self.model = data_model

    def predict(self, station, future_time):
        time_list = []
        time_list.append(future_time)
        result = self.predict_helper(station, time_list)
        return result


    def predict_5d(self, station):
        current_time = datetime.now()
        time_list = []
        for x in range(1, 24 * 5):
            time_list.append(current_time + timedelta(hours=1*x))
        result = self.predict_helper(station, time_list)
        return result

    def predict_24h(self, station):
        current_time = datetime.now()
        time_list = []
        for x in range(1, 24 * 1):
            time_list.append(current_time + timedelta(hours=1*x))
        result = self.predict_helper(station, time_list)
        return result

    def predict_helper(self, station, time_list):
        data_list = []
        for t in time_list:
            data_list.append({"time": t})

        weathers_from_API = requests.get(weatherForecastAPI)
        weathers = json.loads(weathers_from_API.text)

        for input_data in data_list:
            input_data.update(station)
            for weather in weathers["list"]:
                weather["gap"] = abs(weather["dt"] - int(input_data["time"].timestamp()))
            weathersList_sorted = sorted(weathers["list"], key=lambda x: x["gap"])
            weather = weathersList_sorted[0]

            input_data["last_update"] = input_data["time"] # datetime
            input_data["temp"] = weather["main"]["temp"]
            input_data["humidity"] = weather["main"]["humidity"]
            input_data["visibility"] = weather["visibility"]
            input_data["windSpeed"] = weather["wind"]["speed"]
            input_data["windDeg"] = weather["wind"]["deg"]
            weatherMain = weather["weather"][0]["main"]
            # Set initial values to 0
            input_data['weatherMain_Clouds'] = 0
            input_data['weatherMain_Drizzle'] = 0
            input_data['weatherMain_Fog'] = 0
            input_data['weatherMain_Mist'] = 0
            input_data['weatherMain_Rain'] = 0
            input_data['weatherMain_Snow'] = 0
            # Check if weatherMain equals a specific description and set the corresponding variable to 1
            if weatherMain == "Clouds":
                input_data['weatherMain_Clouds'] = 1
            elif weatherMain == "Drizzle":
                input_data['weatherMain_Drizzle'] = 1
            elif weatherMain == "Fog":
                input_data['weatherMain_Fog'] = 1
            elif weatherMain == "Mist":
                input_data['weatherMain_Mist'] = 1
            elif weatherMain == "Rain":
                input_data['weatherMain_Rain'] = 1
            elif weatherMain == "Snow":
                input_data['weatherMain_Snow'] = 1

        data = pd.DataFrame(data_list)
        data["hour"] = data["last_update"].dt.hour
        data["day_of_week"] = data["last_update"].dt.dayofweek
        data["is_weekend"] = data["day_of_week"].isin([5, 6]).astype(int)
        data["month"] = data["last_update"].dt.month
        data['last_update'] = pd.to_datetime(data['last_update'])
        data['last_update'] = data['last_update'].view('int64') // 10**9

        features = ['number', 'position_lat', 'position_lng', 'bike_stands', 'last_update',
                    'temp', 'humidity', 'visibility', 'windSpeed', 'windDeg', 'hour',
                    'day_of_week', 'is_weekend', 'month', 'weatherMain_Clouds',
                    'weatherMain_Drizzle', 'weatherMain_Fog', 'weatherMain_Mist',
                    'weatherMain_Rain', 'weatherMain_Snow']

        data = data[features]
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        # need to do data process

        predicted_bikes = self.model.predict(data_scaled)
        # change to python list
        predicted_bikes = predicted_bikes.tolist()
        # combine the result
        result = data[['last_update']].copy()
        # Convert the 'last_update' column from timestamp integers to datetime objects
        # result['time'] = pd.to_datetime(data['last_update'], unit='s')
        result.loc[:, 'time'] = pd.to_datetime(result['last_update'], unit='s')

        # Format the datetime objects to the desired format
        result['time'] = result['time'].dt.strftime('%m-%d %H:00')
        result["bikes"] = predicted_bikes
        result["bike_stands"] = data["bike_stands"]
        # restrict bikes in the range of [0, bike_stands] and get round value
        result["bikes"] = np.round(np.clip(result["bikes"], 0, result["bike_stands"])).astype(int)
        result["stands"] = result["bike_stands"] - result["bikes"].astype(int)
        result = result.drop('bike_stands', axis=1)
        result = result.drop('last_update', axis=1)
        # Convert the combined DataFrame to a JSON-style list
        json_style_list = result.to_dict(orient='records')

        return json_style_list

class RecommendService:
    # def __int__(self):
    #     self.stations = DatbaseService.get_stations_static()
    @classmethod
    def recommend(cls, location, time):
        """
        :param location: (lat,lng)
        :param time: datetime in the format %Y-%m-%d %H:%M
        :return: station number
        """
        stations_info = DatbaseService.get_stations_static()
        destinations = []
        destinations_lat_lng = []
        for s in stations_info:
            destinations.append((s["number"], s["position_lat"], s["position_lng"]))
            destinations_lat_lng.append((s["position_lat"], s["position_lng"]))

        # print("Destinations:", destinations)
        # print("Destinations Lat/Lng:", destinations_lat_lng)
        # limit 25
        # need to do..
        destinations_lat_lng = destinations_lat_lng[:10]
        destinations = destinations[:10]
        distance_data = cls.get_distance_matrix(location, destinations_lat_lng)

        print("Distance Data:", distance_data)

        distances = []
        for i, destination in enumerate(destinations):
            distance_text = distance_data["rows"][0]["elements"][i]["distance"]["text"]
            distance_value = distance_data["rows"][0]["elements"][i]["distance"]["value"]
            distances.append((destination, distance_text, distance_value))

        sorted_destinations = sorted(distances, key=lambda x: x[2])

        print("Sorted destinations by distance from the start location:")
        for dest, distance_text, distance_value in sorted_destinations:
            print(f"Destination: {dest}, Distance: {distance_text} ({distance_value} meters)")

    @classmethod
    def get_distance_matrix(cls, start, destinations):
        origin_lat = start[0]
        origin_lng = start[1]
        base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": f"{origin_lat},{origin_lng}",
            "destinations": "|".join([f"{lat},{lng}" for lat, lng in destinations]),
            "key": GoogleMap_API_KEY,
            "mode": "walking"
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")