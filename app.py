from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import db, jwt, Config
from routes.auth_routes import Signup, Login, UserResource
from routes.deck_routes import DecksResource, DeckResource
from routes.flashcard_routes import FlashcardResource, FlashcardDetailResource
from routes.progress_routes import ProgressResource
from routes.stats_routes import UserStatsResource
from routes.dashboard_routes import Dashboard
from config import app, api




# Registering API Endpoints.
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(UserResource, "/user")
api.add_resource(DecksResource, "/decks")
api.add_resource(DeckResource, "/decks/<int:deck_id>")
api.add_resource(FlashcardResource, "/flashcards")
api.add_resource(FlashcardDetailResource, "/flashcards/<int:id>")
api.add_resource(ProgressResource, "/progress")
api.add_resource(UserStatsResource, "/stats")
api.add_resource(Dashboard, "/dashboard")
api.add_resource(UserStatsResource, "/user/stats")

@app.route("/")
def home():
    return "Welcome to FlashLearn API!"

if __name__ == "__main__":
    app.run(debug=True)
