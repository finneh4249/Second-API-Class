from flask import Blueprint
from init import db, bcrypt

from models.user import User
from models.card import Card
from models.comment import Comment

from datetime import date
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    """
    Creates a new database. This involves creating all the tables that are
    defined in the models. This is a one-time operation, and should be run
    only once, ideally when the application is first set up.
    """
    db.create_all()
    print("Database created")

@db_commands.cli.command("drop")
def drop_db():
    """
    This is the 'drop' command, which is used to destroy the database.
    
    This command is used to delete all of the tables in the database.
    This is the opposite of the 'create' command, which creates the tables
    in the first place.
    
    This command is useful for starting over from scratch, or for clearing
    out old data that is no longer needed.
    """
    # Call the `drop_all` method on the database
    # This will delete all of the tables in the database
    db.drop_all()
    
    # Print a message to let the user know what's happened
    print("Database dropped")

@db_commands.cli.command("seed")
def seed_db():
    """
    This is the 'seed' command, which is used to populate the database with
    some initial data. This is useful for setting up the database for the
    first time, or for filling it with some sample data for testing purposes.
    
    This function takes no arguments, and does not return anything. It is
    simply a command that needs to be run once in order to set up the
    database.
    """
    
    # First, we need to create two users
    # The first user will be an admin, and will be able to do administrative
    # things, like creating new users, and deleting existing users
    # The second user will be a regular user, and will not be able to do
    # administrative things
    users = [
        User(
            # The first user will be named 'admin'
            name="admin", 
            # The first user will have the email 'admin@email.com'
            email="admin@email.com", 
            # The first user will have the password 'admin'
            # We need to hash the password before we can store it in the
            # database
            password=bcrypt.generate_password_hash("admin").decode("utf-8"), 
            # The first user will be an admin
            is_admin=True
            ),
        User(
            # The second user will be named 'user'
            name="user", 
            # The second user will have the email 'user@email.com'
            email="user@email.com", 
            # The second user will have the password 'user'
            # We need to hash the password before we can store it in the
            # database
            password=bcrypt.generate_password_hash("user").decode("utf-8"), 
            # The second user will not be an admin
            )
        ]
    
    # Now that we have our users, we can add them to the database
    # We can do this by calling the `add_all` method on the database session
    # and passing it a list of all of the users we want to add
    db.session.add_all(users)
    
    # Next, we need to create some cards
    # These will be tasks that the users need to complete
    cards = [
        Card(
            # The first card will be titled 'Github Operations'
            title = "Github Operations",
            # The first card will have the description 'Perform mandatory github
            # ops on the project'
            description = "Perform mandatory github ops on the project",
            # The first card will have the status 'To Do'
            status = "To Do",
            # The first card will have the priority 'High'
            priority = "High",
            # The first card will have the date of today
            date = date.today(),
            # The first card will be assigned to the first user
            user = users[0]
        ), 
        Card(
            # The second card will be titled 'Initialise the modules'
            title = "Initialise the modules",
            # The second card will have the description 'Perform init operations on
            # the necessary modules'
            description = "Perform init operations on the necessary modules",
            # The second card will have the status 'Ongoing'
            status = "Ongoing",
            # The second card will have the priority 'High'
            priority = "High",
            # The second card will have the date of today
            date = date.today(),
            # The second card will be assigned to the first user
            user = users[0]            
        ), 
        Card(
            # The third card will be titled 'Add comments to code'
            title = "Add comments to code",
            # The third card will have the description 'Add meaningful comments when
            # necessary'
            description = "Add meaningful comments when necessary",
            # The third card will have the status 'To Do'
            status = "To Do",
            # The third card will have the priority 'High'
            priority = "High",
            # The third card will have the date of today
            date = date.today(),
            # The third card will be assigned to the first user
            user = users[1]
            )
        ]
    
        
    # Now that we have our cards, we can add them to the database
    # We can do this by calling the `add_all` method on the database session
    # and passing it a list of all of the cards we want to add
    db.session.add_all(cards)

    comments = [
        Comment(
            date = date.today(),
            # The first comment will be on the first card
            card = cards[0],
            # The first comment will be by the first user
            user = users[0],
            # The first comment will have the message 'Perform mandatory github
            # ops on the project'
            message = "Admin is making a comment on Card 0"
            ),
        Comment(
            date = date.today(),
            # The second comment will be on the first card
            card = cards[1],
            # The second comment will be by the first user
            user = users[0],
            # The second comment will have the message 'Perform mandatory github
            # ops on the project'
            message = "Admin is making a comment on Card 1"
            ),
        Comment(
            date = date.today(),
            # The third comment will be on the first card
            card = cards[0],
            # The third comment will be by the first user
            user = users[1],
            # The third comment will have the message 'Perform mandatory github
            # ops on the project'
            message = "The user is making a comment on Card 0"
            )
    ]

    # Now that we have our comments, we can add them to the database

    db.session.add_all(comments)
    # Finally, we need to commit our changes to the database
    # This will save all of the changes we made in the database
    db.session.commit()
    print("Database seeded")
