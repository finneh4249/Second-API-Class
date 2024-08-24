from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    """
    This class represents the Comment model in the database

    Columns:
    - id: The primary key of the comment
    - message: The message of the comment
    - FK to card_id: The foreign key of the card that the comment belongs to
    - FK to user_id: The foreign key of the user that the comment belongs to
"""

    __tablename__ = "comments"

    # The primary key of the comment
    id = db.Column(db.Integer, primary_key=True)

    # The message of the comment
    message = db.Column(db.String),

    # The foreign key of the card that the comment belongs to
    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), nullable=False)

    # The foreign key of the user that the comment belongs to
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # The relationship between the comment and the card
    card = db.relationship("Card", back_populates="comments")

    # The relationship between the comment and the user
    user = db.relationship("User", back_populates="comments")

class CommentSchema(ma.Schema):
    """
    This class represents the CommentSchema in the database

    This is used to serialize the Comment model into a JSON response
    """

    # The relationship between the comment and the user
    user = fields.Nested("UserSchema", only=("id", "name", "email"))

    # The relationship between the comment and the card
    card = fields.Nested("CardSchema", only=("id", "title"))

    class Meta:
        """
        This is the Meta class for the CommentSchema

        It specifies the fields to include in the JSON response
        """

        # The fields to include in the JSON response
        fields = ("id", "message", "card", "user")

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)