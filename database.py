"""Defines the database models used by the application."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Store sentiment prediction records
class Prediction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    movie_name = db.Column(
        db.String(200)
    )

    review = db.Column(
        db.Text
    )

    prediction = db.Column(
        db.String(50)
    )

    confidence = db.Column(
        db.Float
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )