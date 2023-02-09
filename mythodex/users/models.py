"""SQLAlchemy model for User."""

from datetime import datetime
from flask_bcrypt import Bcrypt
from database import db

bcrypt = Bcrypt()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    bio = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    collections = db.relationship('Collection',
        cascade="all,delete",
                            backref='User',)

    created_items = db.relationship(
        "MagicItem",
        cascade="all,delete",
        backref='user_id',)
    
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    
    last_updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"



