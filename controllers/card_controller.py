from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, card_schema, cards_schema
from models.user import User

from controllers.comment_controller import comment

card = Blueprint("card", __name__, url_prefix="/cards")

card.register_blueprint(comment)

"""
/cards - GET - Returns all cards associated with the user that is logged in
/cards/<int:id> - GET - Returns a single card
/cards - POST - Creates a new card
/cards/<int:id> - PUT, PATCH - Updates a card
/cards/<int:id> - DELETE - Deletes a card
"""

@card.route("/", methods=["GET"])
@jwt_required()
def get_cards_by_user():
    """
    This function returns all the cards associated with the user that is
    currently logged in.

    It first gets the user's id from the JWT token, and then uses that to
    query the database for all cards that have the same user_id. It then
    returns those cards as a JSON response.
    """
    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())

    # Query the database for all cards that have the same user_id as the
    # user that is currently logged in
    cards = Card.query.filter_by(user_id=user.id).all()

    # Return the cards as a JSON response
    return cards_schema.jsonify(cards)


@card.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_card(id):
    """
    This function is used to get a single card by id.

    It first gets the card with the given id from the database.
    If the card doesn't exist, it will return a 404 error.

    It then checks if the user that is currently logged in is the same
    as the user that the card belongs to. If not, it will return a 401
    error.

    If the user is authorized, it will return the card as a JSON response.
    """
    # Get the card with the given id from the database
    card = Card.query.get(id)

    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())

    # Check if the card doesn't exist
    if not card:
        # If the card doesn't exist, return a 404 error
        return {"message": "404, Card not found"}, 404
    
    # Check if the user is authorized to view this card
    if user.id != card.user_id:
        # If the user is not authorized, return a 401 error
        return {"message": "Unauthorized"}, 401
    
    # If the user is authorized, return the card as a JSON response
    return card_schema.jsonify(card)

@card.route("/", methods=["POST"])
@jwt_required()
def create_card():
    """
    This function is called when a POST request is sent to the root of the
    /cards endpoint. This is used to create a new card in the database.

    The request must include a JSON payload with the following fields:
    - title: The title of the new card
    - description: The description of the new card
    - status: The status of the new card
    - priority: The priority of the new card

    The function does the following:
    1. Gets the user that is currently logged in
    2. Creates a new card with the given title, description, status, and priority
    3. Sets the date of the new card to today
    4. Sets the user of the new card to the user that is currently logged in
    5. Commits the new card to the database
    6. Returns the new card as a JSON response
    """
    user = User.query.get(get_jwt_identity())

    body = card_schema.load(request.json)

    # Get the title, description, status, and priority from the JSON payload
    title = body["title"]
    description = body["description"]
    status = body["status"]
    priority = body["priority"]

    # Create a new card with the given title, description, status, and priority
    today = date.today()
    new_card = Card(title=title, description=description, status=status, priority=priority, date=today, user=user)

    # Commit the new card to the database
    db.session.add(new_card)
    db.session.commit()

    # Return the new card as a JSON response
    return card_schema.jsonify(new_card)


@card.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_card(id):
    """
    This function is called when a PUT or PATCH request is sent to a card with
    a given id. This is used to update an existing card in the database.

    The request must include a JSON payload with the fields to update, which are
    the following:
    - title: The title of the card
    - description: The description of the card
    - status: The status of the card
    - priority: The priority of the card
    - date: The date of the card

    The function does the following:
    1. Gets the user that is currently logged in
    2. Gets the card with the given id from the database
    3. Checks if the user is authorized to update the card, and if not, returns
    an error message with a 401 status code
    4. If the request is a PATCH, it updates the fields specified in the JSON
    payload.
    5. If the request is a PUT, it updates all the fields with the ones specified
    in the JSON payload.
    6. Commits the updated card to the database
    7. Returns the updated card as a JSON response
    """
    user = User.query.get(get_jwt_identity())
    card = Card.query.get(id)

    # Check if the card doesn't exist
    if not card:
        # If the card doesn't exist, return an error message with a 404 status code
        return {"message": "404, Card not found"}, 404

    # Check if the user is authorized to update the card
    if user.id != card.user_id:
        # If the user is not authorized, return an error message with a 401 status code
        return {"message": "Unauthorized"}, 401
    
    body = card_schema.load(request.json, partial=True)

    card.title = body.get("title") or card.title
    card.description = body.get("description") or card.description
    card.status = body.get("status") or card.status
    card.priority = body.get("priority") or card.priority
    card.date = body.get("date") or card.date

    # Commit the updated card to the database
    db.session.commit()

    # Return the updated card as a JSON response
    return card_schema.jsonify(card)


@card.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_card(id):
    """
    This function is called when a DELETE request is sent to a card with a given id.
    This is used to delete an existing card in the database.

    The function does the following:
    1. Gets the user that is currently logged in
    2. Gets the card with the given id from the database
    3. Checks if the user is authorized to delete the card, and if not, returns
    an error message with a 401 status code
    4. If the user is authorized, it deletes the card from the database
    5. Commits the deletion to the database
    6. Returns a success message as a JSON response
    """
    user = User.query.get(get_jwt_identity())
    card = Card.query.get(id)

    # Check if the card doesn't exist
    if not card:
        # If the card doesn't exist, return a 404 error
        return {"message": "404, Card not found"}, 404
    
    # Check if the user is authorized to delete the card
    if user.id != card.user_id:
        # If the user is not authorized, return an error message with a 401 status code
        return {"message": "Unauthorized"}, 401
    

    
    # Delete the card from the database
    db.session.delete(card)
    
    # Commit the deletion to the database
    db.session.commit()

    # Return a success message as a JSON response
    return {"message": f"Card {card.title} deleted successfully"}
