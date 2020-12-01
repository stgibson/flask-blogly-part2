"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """
        Schema for the users table in the db. Contains id, the user's first and
        last name and a url to an image of the user's profile.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    first_name = db.Column(db.Text, nullable=False)
    
    last_name = db.Column(db.Text, nullable=False)
    
    image_url = db.Column(db.Text, nullable=True)

    @property
    def full_name(self):
        """
            Gets the user's first and last name concatenated. This way, if
            the format for names changes, the update only needs to be reflected
            in this method.
            rtype: str
        """
        return f"{self.first_name} {self.last_name}"