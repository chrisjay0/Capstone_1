"""SQLAlchemy model for Lists."""

from app import db

from datetime import datetime



# db = SQLAlchemy()
    
    
class ItemUserList(db.Model):
    """Mapping Items to User Lists"""
    
    __tablename__ = 'item_lists'
    
    item_id = db.Column(
        db.Integer,
        db.ForeignKey('magic_items.id', 
                      ondelete='cascade',),
        primary_key=True,
    )
    
    list_id = db.Column(
        db.Integer,
        db.ForeignKey('lists.id', 
                      ondelete='cascade',),
        primary_key=True,
    )
    
    times_on_list = db.Column(
        db.Integer,
    )

class UserList(db.Model):
    """A List of Items Made by a User."""

    __tablename__ = 'lists'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    desc = db.Column(db.Text)
    
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
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', 
                      ondelete='cascade',),
        nullable=False,
    )

    user = db.relationship('User',)

    items = db.relationship(
        "MagicItem",
        secondary="item_lists",
        primaryjoin=(ItemUserList.item_id == id),
        secondaryjoin=(ItemUserList.list_id == id),
        cascade="all,delete",
    )
    
    