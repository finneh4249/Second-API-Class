from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card
from models.user import User
from models.comment import Comment, comment_schema, comments_schema


comment = Blueprint("comment", __name__, url_prefix="/comments")


@comment.route("/", methods=["GET"])
@jwt_required()
def get_comments_by_user():
    """
    This function returns all the comments associated with the user that is
    currently logged in.

    It first gets the user's id from the JWT token, and then uses that to
    query the database for all comments that have the same user_id. It then
    returns those comments as a JSON response.
    """
    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())

    # Query the database for all comments that have the same user_id as the
    # user that is currently logged in
    comments = Comment.query.filter_by(user_id=user.id).all()

    # Return the comments as a JSON response
    return comments_schema.jsonify(comments)


@comment.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_comment(id):
    """
    This function is used to get a single comment by id.

    It first gets the comment with the given id from the database.
    If the comment doesn't exist, it will return a 404 error.

    It then checks if the user that is currently logged in is the same\
    as the user that the comment belongs to. If not, it will return a 401
    error.

    If the user is authorized, it will return the comment as a JSON response.
    """
    # Get the comment with the given id from the database
    comment = Comment.query.get(id)

    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())\
    
    # Check if the comment exists
    if not comment:
        # If not, return a 404 error
        return {"message": "Comment not found"}, 404

    # Check if the user that is currently logged in is the same as the user
    # that the comment belongs to
    if user.id != comment.user_id:
        # If not, return a 401 error
        return {"message": "Unauthorized"}, 401

    # Return the comment as a JSON response
    return comment_schema.jsonify(comment)


@comment.route("/", methods=["POST"])
@jwt_required()
def create_comment():
    """
    This function is used to create a new comment.

    It first gets the card with the given id from the database.
    If the card doesn't exist, it will return a 404 error.

    It then checks if the user that is currently logged in is the same
    as the user that the card belongs to. If not, it will return a 401
    error.

    If the user is authorized, it will create a new comment with the
    given message and card id, and return the created comment as a JSON
    response.
    """
    # Get the card with the given id from the database
    card = Card.query.get(request.json["card_id"])

    # Check if the card exists
    if not card:
        # If not, return a 404 error
        return {"message": "Card not found"}, 404

    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())

    # Check if the user that is currently logged in is the same as the user
    # that the card belongs to
    if user.id != card.user_id:
        # If not, return a 401 error
        return {"message": "Unauthorized"}, 401

    # Create a new comment with the given message and card id
    new_comment = Comment(
        message=request.json["message"],
        card_id=request.json["card_id"],
        user_id=user.id
    )

    # Add the new comment to the database
    db.session.add(new_comment)
    db.session.commit()

    # Return the created comment as a JSON response
    return comment_schema.jsonify(new_comment)


@comment.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_comment(id):
    """
    This function is used to delete a comment by id.

    It first gets the comment with the given id from the database.
    If the comment doesn't exist, it will return a 404 error.

    It then checks if the user that is currently logged in is the same
    as the user that the comment belongs to. If not, it will return a 401
    error.

    If the user is authorized, it will delete the comment from the database
    and return a success message as a JSON response.
    """
    # Get the comment with the given id from the database
    comment = Comment.query.get(id)

    # Check if the comment exists
    if not comment:
        # If not, return a 404 error
        return {"message": "Comment not found"}, 404
    
    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())

    # Check if the user that is currently logged in is the same as the user
    # that the comment belongs to
    if user.id != comment.user_id:
        # If not, return a 401 error
        return {"message": "Unauthorized"}, 401
    
    # Delete the comment from the database
    db.session.delete(comment)
    db.session.commit()

    # Return a success message as a JSON response
    return {"message": "Comment deleted successfully"}

