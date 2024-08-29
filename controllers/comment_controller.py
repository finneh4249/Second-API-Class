from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.card import Card
from models.user import User
from models.comment import Comment, comment_schema, comments_schema


comment = Blueprint("comment", __name__, url_prefix="/<int:card_id>/comments")


@comment.route("/", methods=["GET"])
@jwt_required()
def get_comments_by_card(card_id):
    """
    This function returns all the comments associated with the user that is
    currently logged in.

    It first gets the user's id from the JWT token, and then uses that to
    query the database for all comments that have the same user_id. It then
    returns those comments as a JSON response.
    """
    # Get the user that is currently logged in
    user = User.query.get(get_jwt_identity())
    card = Card.query.get(card_id)

    # Query the database for all comments that have the same user_id as the
    # user that is currently logged in
    comments = Comment.query.filter_by(card_id=card.id).all()

    # Return the comments as a JSON response
    return comments_schema.jsonify(comments)


@comment.route("/", methods=["POST"])
@jwt_required()
def create_comment(card_id):
    card = Card.query.get(card_id)

    if not card:
        return {"message": "Card not found"}, 404

    user = User.query.get(get_jwt_identity())

    if user.id != card.user_id:
        return {"message": "Unauthorized"}, 401

    new_comment = Comment(
        date = date.today(),
        message=request.json["message"],
        card_id=card.id,
        user_id=user.id
    )

    db.session.add(new_comment)
    db.session.commit()

    return comment_schema.jsonify(new_comment), 201


@comment.route("/<int:id>", methods=["DELETE"])
@jwt_required() 
def delete_comment(card_id, comment_id):
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
    comment = Comment.query.get(comment_id)

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

@comment.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_comment(card_id, comment_id):
    """
    This function is used to update a comment by id.

    It first gets the comment with the given id from the database.
    If the comment doesn't exist, it will return a 404 error.

    It then checks if the user that is currently logged in is the same
    as the user that the comment belongs to. If not, it will return a 401
    error.

    If the user is authorized, it will update the comment in the database
    and return a success message as a JSON response.
    """
    # Get the comment with the given id from the database
    comment = Comment.query.get(comment_id)

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
    
    # Update the comment in the database
    comment.message = request.json["message"]

    db.session.commit()

    # Return a success message as a JSON response
    return {"message": "Comment updated successfully"}
