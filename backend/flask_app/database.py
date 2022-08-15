from flask_sqlalchemy import SQLAlchemy
from flask_app import db
from models import User, Flight

db.drop_all()
db.create_all()
u1 = User(cell='12312312312', carrier='T-Mobile')
u2 = User(cell='22312312312', carrier='T-Mobile')
f1 = Flight(number='f188', airline='Frontier')
f2 = Flight(number='f198', airline='Frontier')
db.session.add_all([u1, u2, f1, f2])
db.session.commit()
