from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))


class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50))
    category = db.Column(db.String(50))
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime)
    updated_at = db.Column(db.DateTime, default=datetime, onupdate=datetime)

