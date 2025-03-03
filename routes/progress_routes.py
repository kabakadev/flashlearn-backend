from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import Progress, UserStats

class ProgressResource(Resource):
    @jwt_required()
    def get(self, deck_id=None, flashcard_id=None):
        """
        Retrieve progress for a specific deck or flashcard for the authenticated user.
        """
        user_id = get_jwt_identity().get("id")
        
        query = Progress.query.filter_by(user_id=user_id)

        if deck_id:
            query = query.filter_by(deck_id=deck_id)
        if flashcard_id:
            query = query.filter_by(flashcard_id=flashcard_id)

        progress_entries = query.all()

        if not progress_entries:
            return {"message": "No progress found."}, 200

        return [
            {
                "id": p.id,
                "deck_id": p.deck_id,
                "flashcard_id": p.flashcard_id,
                "study_count": p.study_count,
                "correct_attempts": p.correct_attempts,
                "incorrect_attempts": p.incorrect_attempts,
                "total_study_time": p.total_study_time,
                "last_studied_at": p.last_studied_at.isoformat() if p.last_studied_at else None,
                "next_review_at": p.next_review_at.isoformat() if p.next_review_at else None,
                "review_status": p.review_status,
                "is_learned": p.is_learned
            }
            for p in progress_entries
        ], 200
