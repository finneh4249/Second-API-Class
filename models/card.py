from init import db, ma
from marshmallow import fields

class Card(db.Model):
    """
    This class represents the Card model in the database

    Columns:
    - id: The primary key of the card
    - title: The title of the card
    - description: The description of the card
    - status: The status of the card
    - priority: The priority of the card
    - date: The date of the card
    - user_id: The foreign key of the user that the card belongs to
    """

    __tablename__ = "cards"

    # The primary key of the card
    id = db.Column(db.Integer, primary_key=True)

    # The title of the card
    title = db.Column(db.String, nullable=False)

    # The description of the card
    description = db.Column(db.String)

    # The status of the card
    status = db.Column(db.String)

    # The priority of the card
    priority = db.Column(db.String)

    # The date of the card
    date = db.Column(db.Date)

    # The foreign key of the user that the card belongs to
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # The relationship between the card and the user
    user = db.relationship("User", back_populates="cards")

class CardSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=("id", "name", "email"))
    class Meta:
        fields = ("id", "title", "description", "status", "priority", "date", "user")

    

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
