from flask import request, Flask
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, Flashcard, Deck
from flask_cors import  CORS

app = Flask(__name__)

CORS(app)

class FlashcardListResource(Resource):
    #@cross_origin()
    @jwt_required()
    def get(self, deck_id):
        """Retrieve all flashcards for a specific deck (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")

        deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()
        if not deck:
            return {"error": "Deck not found or unauthorized"}, 404

        flashcards = Flashcard.query.filter_by(deck_id=deck_id).all()

        return [
            {
                "id": card.id,
                "question": card.question,
                "answer": card.answer,
                "hint": card.hint,
                "difficulty": card.difficulty,
                "deck_id": card.deck_id,
                "created_at": card.created_at.isoformat(),
                "updated_at": card.updated_at.isoformat(),
            }
            for card in flashcards
        ], 200

    @jwt_required()
    def post(self, deck_id):
        """Create a new flashcard in a specific deck (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")
        data = request.get_json()

        deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()
        if not deck:
            return {"error": "Deck not found or unauthorized"}, 404

        required_fields = ["question", "answer", "difficulty"]
        if not all(field in data and data[field] for field in required_fields):
            return {"error": "Question, answer, and difficulty are required"}, 400

        try:
            new_card = Flashcard(
                question=data["question"],
                answer=data["answer"],
                hint=data.get("hint", ""),  # Optional
                difficulty=data["difficulty"],
                deck_id=deck_id
            )
            db.session.add(new_card)
            db.session.commit()

            return {
                "id": new_card.id,
                "question": new_card.question,
                "answer": new_card.answer,
                "hint": new_card.hint,
                "difficulty": new_card.difficulty,
                "deck_id": new_card.deck_id,
                "created_at": new_card.created_at.isoformat(),
                "updated_at": new_card.updated_at.isoformat(),
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"error": "Flashcard creation failed due to a database error"}, 500


class FlashcardResource(Resource):
    @jwt_required()
    def get(self, deck_id, card_id):
        """Retrieve a single flashcard by ID (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")

        deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()
        if not deck:
            return {"error": "Deck not found or unauthorized"}, 404

        card = Flashcard.query.filter_by(id=card_id, deck_id=deck_id).first()
        if not card:
            return {"error": "Flashcard not found"}, 404

        return {
            "id": card.id,
            "question": card.question,
            "answer": card.answer,
            "hint": card.hint,
            "difficulty": card.difficulty,
            "deck_id": card.deck_id,
            "created_at": card.created_at.isoformat(),
            "updated_at": card.updated_at.isoformat(),
        }, 200

    @jwt_required()
    def put(self, deck_id, card_id):
        """Update an existing flashcard (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")
        data = request.get_json()

        deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()
        if not deck:
            return {"error": "Deck not found or unauthorized"}, 404

        card = Flashcard.query.filter_by(id=card_id, deck_id=deck_id).first()
        if not card:
            return {"error": "Flashcard not found"}, 404

        for field in ["question", "answer", "hint", "difficulty"]:
            if field in data:
                setattr(card, field, data[field])

        db.session.commit()

        return {
            "id": card.id,
            "question": card.question,
            "answer": card.answer,
            "hint": card.hint,
            "difficulty": card.difficulty,
            "updated_at": card.updated_at.isoformat(),
        }, 200

    @jwt_required()
    def delete(self, deck_id, card_id):
        """Delete an existing flashcard (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")

        deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()
        if not deck:
            return {"error": "Deck not found or unauthorized"}, 404

        card = Flashcard.query.filter_by(id=card_id, deck_id=deck_id).first()
        if not card:
            return {"error": "Flashcard not found"}, 404

        db.session.delete(card)
        db.session.commit()

        return {"message": "Flashcard deleted successfully"}, 200
