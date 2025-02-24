from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.init_app(app) 
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)


if __name__ == "__main__":
    