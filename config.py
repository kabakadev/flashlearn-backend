<<<<<<< HEAD
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
=======
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
>>>>>>> experimental_changes
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

<<<<<<< HEAD
app = Flask(__name__)
from datetime import timedelta

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=8)  # Extend to 8 hours

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashlearn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretkey') 

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)


CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
# Default decks template
DEFAULT_DECKS_TEMPLATE = [
    {
        "title": "Default Deck 1",
        "description": "This is a default deck",
        "subject": "General",
        "category": "Default",
        "difficulty": 1,
        "flashcards": [
            {"front_text": "What is 2 + 2?", "back_text": "4"},
            {"front_text": "What is the capital of France?", "back_text": "Paris"}
        ]
    },
    {
        "title": "Default Deck 2",
        "description": "This is another default deck",
        "subject": "General",
        "category": "Default",
        "difficulty": 2,
        "flashcards": [
            {"front_text": "What is 3 * 3?", "back_text": "9"},
            {"front_text": "What is the largest planet?", "back_text": "Jupiter"}
        ]
    }
]
=======
db = SQLAlchemy()
api = Api()
jwt = JWTManager()

def init_extensions(app):
    """Initialize extensions with the Flask app."""
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True, resources=Config.CORS_RESOURCES)
>>>>>>> experimental_changes
