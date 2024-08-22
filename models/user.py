from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
class UserSchema(ma.Schema): 

    class Meta:
        cards = fields.List(fields.Nested("CardSchema", exclude=["user"]))
        fields = ("id", "name", "email", "password", "is_admin")

user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(exclude=["password"], many=True)

