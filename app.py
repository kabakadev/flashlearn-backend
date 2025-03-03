from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import db, jwt, Config
from routes.auth_routes import Signup, Login
from routes.deck_routes import DeckListResource, DeckResource
from routes.flashcard_routes import FlashcardListResource, FlashcardResource

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Extensions
db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
api.init_app(app)

# Import models AFTER initializing db to avoid circular import issues
from models import User, Deck, Flashcard

# Register API Endpoints
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(DeckListResource, "/decks")
api.add_resource(DeckResource, "/decks/<int:deck_id>")
api.add_resource(FlashcardListResource, "/decks/<int:deck_id>/flashcards")
api.add_resource(FlashcardResource, "/decks/<int:deck_id>/flashcards/<int:card_id>")

@app.route("/")
def home():
    return "Welcome to FlashLearn API!"


if __name__ == "__main__":
    app.run(debug=True)
