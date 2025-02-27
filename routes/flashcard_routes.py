from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Flashcard, Deck


flashcard_bp = Blueprint("flashcards", __name__)

# to create a flashcard
@flashcard_bp.route("/create", methods=["POST"])
@jwt_required()
def create_flashcard():
    user_id = get_jwt_identity()
    data = request.json

    # Validating input
    if not data.get("deck_id") or not data.get("front_text") or not data.get("back_text"):
        return jsonify({"error": "All fields are required"}), 400

    deck = Deck.query.filter_by(id=data["deck_id"], user_id=user_id).first()
    if not deck:
        return jsonify({"error": "Deck not found or unauthorized"}), 403

    flashcard = Flashcard(
        deck_id=data["deck_id"],
        front_text=data["front_text"],
        back_text=data["back_text"]
    )
    db.session.add(flashcard)
    db.session.commit()
    return jsonify({"message": "Flashcard created", "id": flashcard.id}), 201
