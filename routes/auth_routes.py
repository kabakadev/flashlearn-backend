from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models import User



@route("/register", methods=["POST"])
def register():
    data = request.json
    user = User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first()
    
    