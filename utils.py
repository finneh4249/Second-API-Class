from flask_jwt_extended import get_jwt_identity

from init import db
from models.user import User

def auth_as_admin():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    return user.is_admin


    