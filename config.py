import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    SQLALCHEMY_DATABASE_URI = "sqlite:///flashlearn.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)  # Token expires in 8 hours
    CORS_RESOURCES = {r"/*": {"origins": "*"}}  # Allow all origins


# Flask Extensions (initialized without app to enable factory pattern)
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
api = Api()
jwt = JWTManager()

def init_extensions(app):
    """Initialize extensions with the Flask app."""
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True, resources=Config.CORS_RESOURCES)
