import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///flashlearn.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")


db = SQLAlchemy()
api = Api()
jwt = JWTManager()

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})