from init import db, jwt, bcrypt

from models.user import User, user_schema, users_schema

from flask import Blueprint, request
from flask_jwt_extended import create_access_token

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return {"message": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.id)

    return {"access_token": access_token}


@auth.route("/register", methods=["POST"])
def register():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()

    if user:
        return {"message": "User already exists"}, 400

    new_user = User(name=name, email=email, password=bcrypt.generate_password_hash(password).decode("utf-8"))

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)