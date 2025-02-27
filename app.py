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
    
    
    with app.app_context():
        # Importing models 
        from models import User, Deck, Flashcard, Progress
        
        
        db.create_all()
        
        
        from routes.auth_routes import auth_bp
        from routes.deck_routes import deck_bp

        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(deck_bp, url_prefix="/decks")

    
    @app.route("/")
    def home():
        return "Welcome to FlashLearn API!"
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)