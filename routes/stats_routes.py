from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import db
from models import UserStats

class UserStatsResource(Resource):
    @jwt_required()
    def put(self):
        """Update user stats, such as weekly goal."""
        user_id = get_jwt_identity().get("id")
        data = request.get_json()

        # Fetch or create user stats
        stats = UserStats.query.filter_by(user_id=user_id).first()
        if not stats:
            stats = UserStats(user_id=user_id)
            db.session.add(stats)
