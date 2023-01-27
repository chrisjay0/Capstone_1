"""SQLAlchemy models for Magic Items."""


from datetime import datetime

from app import db
    
class ItemVariant(db.Model):
    """Mapping Magic Items to the Magic Item of which they are a variant."""

    __tablename__ = 'item_variants'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    
    original_item_name = db.Column(
        db.Text,
        nullable=False,
    )
    
    variant_item_name = db.Column(
        db.Text,
        nullable=False,
    )

class MagicItem(db.Model):
    """MagicItem."""

    __tablename__ = 'magic_items'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    item_type = db.Column(
        db.Text,
        nullable=False,
    )

    rarity = db.Column(
        db.Text,
        nullable=False,
    )

    has_variants = db.Column(
        db.Boolean,
    )

    is_variant = db.Column(
        db.Boolean,
    )

    description = db.Column(
        db.Text,
    )

    created_by_username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=True,
        default=None,
    )

    source = db.Column(
        db.Text,
        nullable=False,
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

    # lists = db.relationship(
    #     "UserList",
    #     secondary="item_lists",
    #     primaryjoin=(ItemUserList.list_id == id),
    #     secondaryjoin=(ItemUserList.item_id == id),
    #     cascade="all,delete",
    # )
    
    # user_list = db.relationship('ItemUserList',
    #                               backref='list')

    # lists = db.relationship('UserList',
    #                            secondary='item_lists',
    #                            backref='lists')

    def __repr__(self):
        return f"<Magic Item #{self.id}: {self.name}, {self.item_type}>"