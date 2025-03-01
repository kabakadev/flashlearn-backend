from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, Flashcard, Deck, User


class FlashcardListResource(Resource):
    @jwt_required()
    def get(self, deck_id):
        """Retrieve all flashcards for a specific deck (only if the user owns the deck)."""
        user_id = get_jwt_identity().get("id")

        # Verify deck belongs to user
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


# Update a flashcard
@flashcard_bp.route("/update/<int:flashcard_id>", methods=["PUT"])
@jwt_required()
def update_flashcard(flashcard_id):
    user_id = get_jwt_identity()
    data = request.json

    flashcard = Flashcard.query.join(Deck).filter(
        Flashcard.id == flashcard_id,
        Deck.user_id == user_id
    ).first()

    if not flashcard:
        return jsonify({"error": "Flashcard not found or unauthorized"}), 403

    flashcard.front_text = data.get("front_text", flashcard.front_text)
    flashcard.back_text = data.get("back_text", flashcard.back_text)

    db.session.commit()
    return jsonify({"message": "Flashcard updated"}), 200

# Delete a flashcard
@flashcard_bp.route("/delete/<int:flashcard_id>", methods=["DELETE"])
@jwt_required()
def delete_flashcard(flashcard_id):
    user_id = get_jwt_identity()

    flashcard = Flashcard.query.join(Deck).filter(
        Flashcard.id == flashcard_id,
        Deck.user_id == user_id
    ).first()

    if not flashcard:
        return jsonify({"error": "Flashcard not found or unauthorized"}), 403

    db.session.delete(flashcard)
    db.session.commit()
    return jsonify({"message": "Flashcard deleted"}), 200
