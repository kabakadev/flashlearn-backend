from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Deck

deck_bp = Blueprint("decks", __name__)

# Create a Deck
@deck_bp.route("/", methods=["POST"])
@jwt_required()
def create_deck():
    user_id = get_jwt_identity()  # to get logged-in user ID
    data = request.json
    
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_deck = Deck(
        user_id=user_id,
        title=data["title"],
        description=data.get("description"),
        subject=data.get("subject"),
        category=data.get("category"),
        difficulty=data.get("difficulty")
    )

    db.session.add(new_deck)
    db.session.commit()
    return jsonify({"message": "Deck created successfully", "deck_id": new_deck.id}), 201

