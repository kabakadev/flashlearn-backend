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

# Retrieve all flashcards in a deck
@flashcard_bp.route("/deck/<int:deck_id>", methods=["GET"])
@jwt_required()
def get_flashcards(deck_id):
    user_id = get_jwt_identity()
    deck = Deck.query.filter_by(id=deck_id, user_id=user_id).first()
    
    if not deck:
        return jsonify({"error": "Deck not found or unauthorized"}), 403

    flashcards = Flashcard.query.filter_by(deck_id=deck_id).all()
    return jsonify([{
        "id": fc.id,
        "front_text": fc.front_text,
        "back_text": fc.back_text
    } for fc in flashcards]), 200


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
