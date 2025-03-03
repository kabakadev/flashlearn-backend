from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import User, Deck

class Dashboard(Resource):
    @jwt_required()
    def get(self):
        """
        Fetches the logged-in user's dashboard data, including:
        - Total flashcards studied
        - Most reviewed decks
        - Overall progress tracking
        - Study statistics (weekly goal, mastery level, streak, focus, retention, minutes per day)
        """
        user_data = get_jwt_identity()
        user_id = user_data.get("id")
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found"}, 404
        
        # Fetch user's decks
        decks = Deck.query.filter_by(user_id=user_id).all()
        deck_data = []
        total_flashcards_studied = 0
        most_reviewed_deck = None
        most_reviews = 0
        
        for deck in decks:
            progress_entries = Progress.query.filter_by(deck_id=deck.id, user_id=user_id).all()
            deck_study_count = sum(entry.study_count for entry in progress_entries)
            total_flashcards_studied += deck_study_count

            # Track the most reviewed deck
            if deck_study_count > most_reviews:
                most_reviews = deck_study_count
                most_reviewed_deck = deck.title

            deck_data.append({
                "deck_id": deck.id,
                "deck_title": deck.title,
                "flashcards_studied": deck_study_count
            })
        
        