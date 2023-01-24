"""SQLAlchemy models for Magic Items."""


from datetime import datetime

from app import db

from import_services import ItemUserList
    
class ItemVariant(db.Model):
    """Mapping Magic Items to the Magic Item of which they are a variant."""

    __tablename__ = 'item_variants'

    original_item_id = db.Column(
        db.Integer,
        db.ForeignKey('magic_items.id'),
        primary_key=True,
    )
    
    variant_item_id = db.Column(
        db.Integer,
        db.ForeignKey('magic_items.id'),
        primary_key=True,
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

    variants = db.relationship(
        "MagicItem",
        secondary="item_variants",
        primaryjoin=(ItemVariant.original_item_id == id),
        secondaryjoin=(ItemVariant.variant_item_id == id)
    )

    variant_of = db.relationship(
        "MagicItem",
        secondary="item_variants",
        primaryjoin=(ItemVariant.variant_item_id == id),
        secondaryjoin=(ItemVariant.original_item_id == id)
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

    lists = db.relationship(
        "UserList",
        secondary="item_lists",
        primaryjoin=(ItemUserList.list_id == id),
        secondaryjoin=(ItemUserList.item_id == id),
        cascade="all,delete",
    )

    def __repr__(self):
        return f"<Magic Item #{self.id}: {self.name}, {self.item_type}>"