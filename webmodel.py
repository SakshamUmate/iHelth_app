from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
