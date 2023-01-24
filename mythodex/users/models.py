"""SQLAlchemy model for User."""


from datetime import datetime

from flask_bcrypt import Bcrypt

from app import db

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

    lists = db.relationship('UserList',)

    created_item = db.relationship(
        "MagicItem",
    )

    liked_item = db.relationship(
        'MagicItem',
        secondary="item_likes"
    )
    
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )
    
    date_last_updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

class ItemLikes(db.Model):
    """Mapping user liked items to items."""

    __tablename__ = 'item_likes' 

    # id = db.Column(
    #     db.Integer,
    #     primary_key=True
    # )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id',
                      ondelete='cascade',),
        primary_key=True,
        )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey('magic_items.id',
                      ondelete='cascade',),
        primary_key=True,
    )



