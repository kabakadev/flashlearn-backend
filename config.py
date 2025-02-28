from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flashlearn.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_secret_key"

# Extensions
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)
