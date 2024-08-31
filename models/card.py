from init import db, ma
from marshmallow import fields, validates, ValidationError
from marshmallow.validate import Length, And, Regexp, OneOf

VALID_STATUS = ("To Do", "In Progress", "Completed", "Testing", "Deployed")
VALID_PRIORITY = ("Low", "Medium", "High", "Immediate")

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
    comments = db.relationship("Comment", back_populates="card", cascade="all, delete")

class CardSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=("id", "name", "email"))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["card"]))

    title = fields.String(required=True, validate=And(Length(min=4, max=100, error="Title must be between 4 and 100 characters"), Regexp("^[A-Z][a-zA-Z0-9 ]+$", error="Title must contain only alphanumeric characters and start with an uppercase letter")))
    
    status = fields.String(validate=OneOf(VALID_STATUS))
    
    priority = fields.String(validate=OneOf(VALID_PRIORITY))

    @validates("status")
    def validate_status(self, value):
        if value == VALID_STATUS[1]:
            # Check if an existing card has the status "In Progress"
            stmt = db.select(db.func.count()).select_from(Card).where(Card.status == VALID_STATUS[1])
            count = db.session.scalar(stmt)
            if count > 0:
                raise ValidationError("Status cannot be 'In Progress'")
            
        
    
    class Meta:
        fields = ("id", "title", "description", "status", "priority", "date", "user", "comments")

    

card_schema = CardSchema()
cards_schema = CardSchema(many=True)
