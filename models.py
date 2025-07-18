from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask import Flask

db = SQLAlchemy()



class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.Date)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=True)

class Trip(db.Model):

    trip_id = db.Column(db.Integer, primary_key = True)
    trip_name = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100),nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    transactions = db.relationship('Transaction', backref='trip', lazy=True)