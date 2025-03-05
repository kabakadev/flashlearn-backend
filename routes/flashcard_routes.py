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
    def get(self):
        """Retrieve all flashcards for a specific deck (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")

        flashcards = Flashcard.query.join(Deck).filter(Deck.user_id == user_id).all()
        if not flashcards:
            return {"message": "No flashcards found."}, 404

        return [
            {
               "id": card.id,
                "deck_id": card.deck_id,
                "front_text": card.front_text,
                "back_text": card.back_text,
                "created_at": card.created_at.isoformat(),
                "updated_at": card.updated_at.isoformat()
            }
            for card in flashcards
        ], 200

    @jwt_required()
    def post(self):
        """Create a new flashcard in a specific deck (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")
        data = request.get_json()

        deck = Deck.query.filter_by(id=data["deck_id"], user_id=user_id).first()
        if not deck:
            return {"error": "Deck not found or unauthorized"}, 404

        required_fields = ["deck_id", "front_text", "back_text"]
        if not all(field in data and data[field] for field in required_fields):
            return {"error": "All fields are required"}, 400

        try:
            new_card = Flashcard(
                front_text=data["back_text"],
                back_text=data["front_text"],
                deck_id=data["deck_id"]
            )
            db.session.add(new_card)
            db.session.commit()

            return {
                "id": new_card.id,
                "front_text": new_card.front_text,
                "back_text": new_card.back_text,
                "deck_id": new_card.deck_id,
                "created_at": new_card.created_at.isoformat(),
                "updated_at": new_card.updated_at.isoformat(),
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"error": "Flashcard creation failed due to a database error"}, 500


class FlashcardResource(Resource):
    @jwt_required()
    def put(self, deck_id, card_id):
        """Update an existing flashcard (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")
        data = request.get_json()

        card = Flashcard.query.join(Deck).filter(Flashcard.id == id, Deck.user_id == user_id).first()
        if not card:
            return {"error": "Flashcard not found"}, 404
        card.front_text = data.get("front_text", card.front_text)
        card.back_text = data.get("back_text", card.back_text)


        db.session.commit()

        return {
            "id": card.id,
            "deck_id": card.deck_id,
            "front_text": card.front_text,
            "back_text": card.back_text,
            "updated_at": card.updated_at.isoformat()
        }, 200

    @jwt_required()
    def delete(self, deck_id, card_id):
        """Delete an existing flashcard (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")
        card = Flashcard.query.join(Deck).filter(Flashcard.id == id, Deck.user_id == user_id).first()


        if not card:
            return {"error": "card not found"}, 404


        db.session.delete(card)
        db.session.commit()

        return {"message": "Flashcard deleted successfully"}, 200