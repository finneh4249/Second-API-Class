from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card, card_schema, cards_schema
from models.user import User

card = Blueprint("card", __name__, url_prefix="/cards")

@card.route("/", methods=["GET"])
@jwt_required()
def get_cards_by_user():
    user = User.query.get(get_jwt_identity())
    cards = Card.query.filter_by(user_id=user.id).all()
    return cards_schema.jsonify(cards)


@card.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_card(id):
    # if card doesnt exist, return error
    card = Card.query.get(id)

    user = User.query.get(get_jwt_identity())

    if not card:
        return {"message": "404, Card not found"}, 404
    
    if user.id != card.user_id:
        return {"message": "Unauthorized"}, 401
    
    return card_schema.jsonify(card)

@card.route("/", methods=["POST"])
@jwt_required()
def create_card():
    user = User.query.get(get_jwt_identity())

    title = request.json["title"]
    description = request.json["description"]
    status = request.json["status"]
    priority = request.json["priority"]
    today = date.today()

    new_card = Card(title=title, description=description, status=status, priority=priority, date=today, user=user)

    db.session.add(new_card)
    db.session.commit()

    return card_schema.jsonify(new_card)


@card.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_card(id):
    user = User.query.get(get_jwt_identity())
    card = Card.query.get(id)

    # If User is not card user, return error
    if user.id != card.user_id:
        return {"message": "Unauthorized"}, 401

    if request.method == "PATCH":
        if request.json.get("title"):
            card.title = request.json["title"]
        if request.json.get("description"):
            card.description = request.json["description"]
        if request.json.get("status"):
            card.status = request.json["status"]
        if request.json.get("priority"):
            card.priority = request.json["priority"]
        if request.json.get("date"):
            card.date = request.json["date"]
    else:
        card.title = request.json["title"]
        card.description = request.json["description"]
        card.status = request.json["status"]
        card.priority = request.json["priority"]
        card.date = request.json["date"]

    db.session.commit()

    return card_schema.jsonify(card)


@card.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_card(id):
    user = User.query.get(get_jwt_identity())
    # If User is not card user, return error
    if user.id != Card.query.get(id).user_id:
        return {"message": "Unauthorized"}, 401
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()

    return card_schema.jsonify(card)
