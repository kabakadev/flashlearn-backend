import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///flashlearn.db")  # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")

app = Flask(__name__)
# Extensions
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)