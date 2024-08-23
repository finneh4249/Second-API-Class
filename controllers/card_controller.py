from flask import Blueprint, request
from init import db
from models.card import Card, card_schema, cards_schema
from models.user import User, user_schema, users_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

card = Blueprint("card", __name__, url_prefix="/cards")

@card.route("/", methods=["GET"])
def get_cards():
    cards = Card.query.all()
    return cards_schema.jsonify(cards)


@card.route("/<int:id>", methods=["GET"])
def get_card(id):
    card = Card.query.get(id)
    return card_schema.jsonify(card)

@card.route("/user/<int:id>", methods=["GET"])
def get_user_cards(id):
    cards = Card.query.filter_by(user_id=id).all()
    return cards_schema.jsonify(cards)

@card.route("/", methods=["POST"])
def create_card():
    title = request.json["title"]
    description = request.json["description"]
    status = request.json["status"]
    priority = request.json["priority"]
    date = request.json["date"]

    new_card = Card(title=title, description=description, status=status, priority=priority, date=date)

    db.session.add(new_card)
    db.session.commit()

    return card_schema.jsonify(new_card)


@card.route("/<int:id>", methods=["PUT", "PATCH"])
def update_card(id):
    card = Card.query.get(id)

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
