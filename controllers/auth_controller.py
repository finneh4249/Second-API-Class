from init import db, jwt, bcrypt
from models.user import User, user_schema, UserSchema, users_schema

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
def login():
    """
    This is the login route. It's used to login existing users.

    The route expects a JSON payload with the 'email' and 'password' fields.
    It then checks if there is a user in the database with the given email,
    and if the password matches with the one in the database.
    If the credentials are correct, it generates a JWT token with the user's
    id as the payload and returns it with a success message.
    If the credentials are incorrect, it returns an error message with a 401
    status code.
    """
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Get the user from the database with the given email
    user = User.query.filter_by(email=email).first()

    # Check if the user exists and if the password is correct
    if not user or not bcrypt.check_password_hash(user.password, password):
        # If not, return an error message with a 401 status code
        return {"message": "Invalid credentials"}, 401

    # If the credentials are correct, generate a JWT token with the user's id
    # as the payload
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))

    # Return the JWT token with a success message
    return {"message": f"Login successful, welcome back {user.name}", "access_token": access_token}


@auth.route("/register", methods=["POST"])
def register():
    """
    This is the registration route. It's used to create new users.
    """
    body = UserSchema().load(request.json)
    # Get the name, email and password from the request
    name = body.get("name")
    email = body.get("email")
    password = body.get("password")

    # Check if a user with the same email already exists
    user = User.query.filter_by(email=email).first()

    # If the user already exists, return an error
    if user:
        return {"message": "User already exists"}, 400

    # Check if all the required fields are present
    if not name or not email or not password:
        return {"message": "Missing name, email or password"}, 400
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create a new user
    new_user = User(name=name, email=email, password=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)

    # Save the changes
    db.session.commit()

    # Return the new user
    return user_schema.jsonify(new_user)

@auth.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """
    This function is called when a GET request is sent to the /users endpoint.
    It returns a list of all the users in the database.
    """
    users = User.query.all()
    return users_schema.jsonify(users)

@auth.route("/users/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(id):
    """
    This function is called when a PUT or PATCH request is sent to a user with
    a given id. This is used to update an existing user in the database.

    The request must include a JSON payload with the fields to update, which are
    """
    user = User.query.get(id)

    if not user:
        return {"message": "User not found"}, 404

    if user.id != get_jwt_identity():
        return {"message": "Unauthorized"}, 401

    body = UserSchema().load(request.json, partial=True)

    if "name" in body:
        user.name = body["name"]
    if "email" in body:
        user.email = body["email"]
    if "password" in body:
        user.password = bcrypt.generate_password_hash(body["password"]).decode("utf-8")

    db.session.commit()

    return user_schema.jsonify(user)