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

# to get All Decks (for logged-in user)
@deck_bp.route("/", methods=["GET"])
@jwt_required()
def get_decks():
    user_id = get_jwt_identity()
    decks = Deck.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": deck.id,
            "title": deck.title,
            "description": deck.description,
            "subject": deck.subject,
            "category": deck.category,
            "difficulty": deck.difficulty
        }
        for deck in decks
    ]), 200

# to get a Single Deck
@deck_bp.route("/<int:deck_id>", methods=["GET"])
@jwt_required()
def get_deck(deck_id):
    user_id = get_jwt_identity()
    deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()

    if not deck:
        return jsonify({"error": "Deck not found"}), 404

    return jsonify({
        "id": deck.id,
        "title": deck.title,
        "description": deck.description,
        "subject": deck.subject,
        "category": deck.category,
        "difficulty": deck.difficulty
    }), 200

# Update a Deck
@deck_bp.route("/<int:deck_id>", methods=["PUT"])
@jwt_required()
def update_deck(deck_id):
    user_id = get_jwt_identity()
    deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()

    if not deck:
        return jsonify({"error": "Deck not found"}), 404

    data = request.json

    deck.title = data.get("title", deck.title)
    deck.description = data.get("description", deck.description)
    deck.subject = data.get("subject", deck.subject)
    deck.category = data.get("category", deck.category)
    deck.difficulty = data.get("difficulty", deck.difficulty)

    db.session.commit()
    return jsonify({"message": "Deck updated successfully"}), 200


# delete a Deck
@deck_bp.route("/<int:deck_id>", methods=["DELETE"])
@jwt_required()
def delete_deck(deck_id):
    user_id = get_jwt_identity()
    deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()

    if not deck:
        return jsonify({"error": "Deck not found"}), 404

    db.session.delete(deck)
    db.session.commit()
    return jsonify({"message": "Deck deleted successfully"}), 200
