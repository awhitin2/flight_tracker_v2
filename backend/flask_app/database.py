from flask_sqlalchemy import SQLAlchemy
from flask_app import db, models

# db.drop_all()
# db.create_all()
# u1 = User(cell='12312312312', carrier='T-Mobile')
# u2 = User(cell='22312312312', carrier='T-Mobile')
# f1 = Flight(number='f188', airline='Frontier')
# f2 = Flight(number='f198', airline='Frontier')
# db.session.add_all([u1, u2, f1, f2])
# db.session.commit()

def get_flight(airline_code:str, number:str, date_str:str)->models.Flight:
    return models.Flight.query.filter_by(airline_code=airline_code)\
                       .filter_by(number=number)\
                       .filter_by(date_str=date_str)\
                       .first()

def get_all_flights()->list[models.Flight]:
    return models.Flight.query.all()

def set_flight(
    flight_number: str, airline_code: str, date_str: str, flight_info: dict
    )->models.Flight:

    return models.Flight(
            number = flight_number,
            airline_code = airline_code,
            date_str = date_str,
            **flight_info
            # arrived = flight_info['arrived_status']
            )

def update_flight(flight: models.Flight, changes: dict[dict[str:str]])->None:
    for key, value in changes.items():
        setattr(flight, key, value['updated'])
    db.session.commit()

def get_user_(cell:str)->models.User:
    return models.User.query.filter_by(cell=cell).first()

def set_user(cell:str, carrier:str)->models.User:
    return models.User(cell = cell, carrier = carrier)

