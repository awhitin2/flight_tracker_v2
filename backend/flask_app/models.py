
from flask_app import db 

user_flight = db.Table('user_flight',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('flight_id', db.Integer, db.ForeignKey('flight.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell = db.Column(db.String, unique=True, nullable=False)
    carrier = db.Column(db.String, unique=False, nullable=False)
    flights = db.relationship(
        'Flight', secondary=user_flight, back_populates = 'followers'
    )

    def __repr__(self) -> str:
        return f'User: {self.id}, {self.cell}'

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, nullable=False)
    airline_code = db.Column(db.String, nullable=False)
    date_str = db.Column(db.String, nullable=False)
    airline = db.Column(db.String, nullable=False)
    scheduled_departure_time = db.Column(db.String, nullable=False)
    scheduled_arrival_time = db.Column(db.String, nullable=False)
    estimated_arrival_time = db.Column(db.String, nullable=False)
    arrival_airport = db.Column(db.String, nullable=False)
    arrived = db.Column(db.Boolean, nullable=True)
    followers = db.relationship(
        'User', secondary=user_flight, back_populates = 'flights'
    )

    def __repr__(self):
        return f'Flight: {self.airline}{self.number} -- self.date'
