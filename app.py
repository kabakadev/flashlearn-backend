from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

from routes.auth_routes import auth_bp

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return "Welcome to FlashLearn API!"



if __name__ == "__main__":
    app.run(debug=True)