from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from models import db, Deck, User


class DeckListResource(Resource):
    @jwt_required()
    def get(self):
        """Retrieve all decks for the authenticated user."""
        user_id = get_jwt_identity().get("id")
        decks = Deck.query.filter_by(user_id=user_id).all()

        if not decks:
            return {"message": "You have no decks yet."}, 200

        return [
            {
                "id": deck.id,
                "title": deck.title,
                "description": deck.description,
                "subject": deck.subject,
                "category": deck.category,
                "difficulty": deck.difficulty,
                "created_at": deck.created_at.isoformat(),
                "updated_at": deck.updated_at.isoformat(),
            }
            for deck in decks
        ], 200


@jwt_required()
    def post(self):
        """Create a new deck for the authenticated user."""
        data = request.get_json()
        user_id = get_jwt_identity().get("id")

        required_fields = ["title", "description", "subject", "category", "difficulty"]
        if not all(field in data and data[field] for field in required_fields):
            return {"error": "All fields are required"}, 400

        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            new_deck = Deck(
                title=data["title"],
                description=data["description"],
                subject=data["subject"],
                category=data["category"],
                difficulty=data["difficulty"],
                user_id=user_id
            )
            db.session.add(new_deck)
            db.session.commit()

            return {
                "id": new_deck.id,
                "title": new_deck.title,
                "description": new_deck.description,
                "subject": new_deck.subject,
                "category": new_deck.category,
                "difficulty": new_deck.difficulty,
                "created_at": new_deck.created_at.isoformat(),
                "updated_at": new_deck.updated_at.isoformat(),
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {"error": "Deck creation failed due to a database error"}, 500

