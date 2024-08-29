import os

from flask import Flask

from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth
from controllers.card_controller import card
from controllers.comment_controller import comment

def create_app():
    """
    This is the main function for creating a new Flask instance.
    The instance is the main entry point for the application, and
    it's where all the configuration and setup happens.
    """
    # Create a new Flask instance
    app = Flask(__name__)

    # Set the JSON sort keys to False
    # This is necessary for the Marshmallow schema to work correctly
    app.json.sort_keys = False
    
    # Set the secret key for the app
    # This is used for signing sessions and JWTs
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    
    # Set the database URI for the app
    # This is used by SQLAlchemy to connect to the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    
    # Initialise the database
    # This is necessary for the app to be able to use the database
    db.init_app(app)
    
    # Initialise the Marshmallow object
    # This is necessary for serializing and deserializing data
    ma.init_app(app)
    
    # Initialise the Bcrypt object
    # This is necessary for hashing passwords
    bcrypt.init_app(app)
    
    # Initialise the JWTManager object
    # This is necessary for generating and verifying JWTs
    jwt.init_app(app)
    
    # Register the blueprint for the database commands
    # This is necessary for using the database commands
    app.register_blueprint(db_commands)
    
    # Register the blueprint for the authentication controller
    # This is necessary for using the authentication controller
    app.register_blueprint(auth)
    
    # Register the blueprint for the card controller
    # This is necessary for using the card controller
    app.register_blueprint(card)

    # Register the blueprint for the comment controller
    # This is necessary for using the comment controller
    app.register_blueprint(comment)
    
    # Return the app
    return app

