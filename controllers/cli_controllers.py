from flask import Blueprint
from init import db, bcrypt

from models.user import User

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Database created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Database dropped")

@db_commands.cli.command("seed")
def seed_db():
    users = [
        User(
            name="admin", 
            email="admin@email.com", 
            password=bcrypt.generate_password_hash("admin").decode("utf-8"), 
            is_admin=True
            ),
        User(
            name="user", 
            email="user@email.com", 
            password=bcrypt.generate_password_hash("user").decode("utf-8"), 
            )
        ]
        
    db.session.add_all(users)
    db.session.commit()
    print("Database seeded")