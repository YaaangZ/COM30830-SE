from app import db


class Station(db.Model):
    __tablename__ = 'station'
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(128))
    position_lat = db.Column(db.Numeric(8, 6))
    position_lng = db.Column(db.Numeric(8, 6))
    banking = db.Column(db.Integer)
    bonus = db.Column(db.Integer)
    bike_stands = db.Column(db.Integer)

    def __repr__(self):
        return f"<Station number={self.number}, name='{self.name}', " \
               f"address='{self.address}', position=({self.position_lat}, " \
               f"{self.position_lng}), banking={self.banking}, bonus={self.bonus}, bike_stands={self.bike_stands}>"

    def to_dict(self):
        return {
            'number': self.number,
            'name': self.name,
            'address': self.address,
            'position_lat': float(self.position_lat),
            'position_lng': float(self.position_lng),
            'banking': self.banking,
            'bonus': self.bonus,
            'bike_stands': self.bike_stands
        }