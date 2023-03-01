from typing import List, Optional
from models import Station


class StationService:
    def __init__(self, db):
        self.db = db

    def get_station_by_number(self, number: int) -> Optional[Station]:
        return self.db.session.query(Station).filter_by(number=number).all()[0]

    def get_all_stations(self) -> List[Station]:
        return self.db.session.query(Station).all()
