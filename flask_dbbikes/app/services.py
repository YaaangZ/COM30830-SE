from typing import List, Optional
from sqlalchemy import func, text

from models import Station, Availability
from datetime import datetime, timedelta

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


