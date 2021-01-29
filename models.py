"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ Model """
    __tablename__ = "user"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.TEXT,
                    nullable=False,
                    unique=True)
    last_name = db.Column(db.TEXT,
                    nullable=False,
                    unique=True)
    image_url = db.Column(db.TEXT, 
                    nullable=False,
                    unique=False,
                    default= "/static/profile.jpg")

    @property
    def full_name(self):
        """Returns full name"""
        return f"{self.first_name} {self.last_name}"