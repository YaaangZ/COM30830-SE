from typing import List, Optional
from sqlalchemy import func

from models import Station, Availability
from datetime import datetime, timedelta

class StationService:
    def __init__(self, db):
        self.db = db

    def get_station_by_number(self, number: int) -> Optional[Station]:
        return self.db.session.query(Station).filter_by(number=number).all()[0]

    def get_all_stations(self) -> List[Station]:
        return self.db.session.query(Station).all()
class AvailabilityService:
    def __init__(self, db):
        self.db = db
    def get_availability_by_number(self, number: int) -> Optional[Availability]:

        # return self.db.session.query(Availability).filter_by(number=number).first()
        return self.db.session.query(Availability).filter_by(number=number).order_by(Availability.last_update.desc()).first()
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
    # def get_station_detail(self, number):
    #     res = self.db.session.query(
    #         Availability.number, Availability.available_bike_stands, Availability.available_bikes,
    #         Station.name, Station.address, Station.bike_stands, Availability.last_update) \
    #         .join(Station, Availability.number == Station.number) \
    #         .filter(Availability.number == number) \
    #         .order_by(Availability.last_update.desc()) \
    #         .limit(1).first()
    #     return

