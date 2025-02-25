from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initializing extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Importing models and register blueprints
    with app.app_context():
        # Importing models after db is defined 
        from models import User, Deck, Flashcard, Progress
        
        # to create tables if they don't exist
        db.create_all()
        
        
        from routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/auth")
    
    @app.route("/")
    def home():
        return "Welcome to FlashLearn API!"
    
    return app

# to  create the app instance if this file is run directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)