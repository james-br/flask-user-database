"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

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
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Returns full name"""
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Makes post for users"""

    __tablename__ = "posts"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.Text, nullable=False)
    content     = db.Column(db.Text, nullable=False)
    created_at  = db.Column(
                    db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def shows_date(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")




