

from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
import re
from config import db
from models import User

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username, email, password = data.get("username"), data.get("email"), data.get("password")

        if not username or not email or not password:
            return {"error": "Missing required fields"}, 400

        if not is_valid_email(email):
            return {"error": "Invalid email format"}, 400

        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Username or email already exists"}, 409


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/user", methods=["GET"])
@jwt_required()  # Requires valid token
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 200