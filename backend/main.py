from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# CORS(app, resources={r"/*":{'origins':'*'}})


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
    number = db.Column(db.String, unique=False, nullable=False)
    airline = db.Column(db.String, nullable=False)
    # date = db.Column(db.String, nullable=False)
    # scheduled_departure_time = db.Column(db.String, nullable=False)
    # scheduled_arrival_time = db.Column(db.String, nullable=False)
    # estimated_arrival_time = db.Column(db.String, nullable=False)
    # arrival_airport = db.Column(db.String, nullable=False)
    # arrived_status = db.Column(db.Boolean, nullable=False)
    followers = db.relationship(
        'User', secondary=user_flight, back_populates = 'flights'
    )

    def __repr__(self):
        return f'Flight: {self.airline}{self.number} -- self.date'



@app.route('/', methods=['GET'])
def hello_world():
    return("Hello world!")


if __name__ == "__main__":
    # app.run(debug=True)
    db.drop_all()
    db.create_all()
    u1 = User(cell='12312312312', carrier='T-Mobile')
    u2 = User(cell='22312312312', carrier='T-Mobile')
    f1 = Flight(number='f188', airline='Frontier')
    f2 = Flight(number='f198', airline='Frontier')
    db.session.add_all([u1, u2, f1, f2])
    db.session.commit()
    
