from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    seat_row = db.Column(db.Integer)
    seat_col = db.Column(db.Integer)
    price = db.Column(db.Float)
    code = db.Column(db.String(10), unique=True)