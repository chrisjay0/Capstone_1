"""SQLAlchemy models for Magic Items."""
from datetime import datetime
from database import db


class ItemVariant(db.Model):
    """Mapping Magic Items to the Magic Item of which they are a variant."""

    __tablename__ = "items_variants"

    original_item_id = db.Column(
        db.Integer,
        db.ForeignKey("magic_items.id", ondelete="cascade"),
        primary_key=True,
    )

    variant_item_id = db.Column(
        db.Integer,
        db.ForeignKey("magic_items.id", ondelete="cascade"),
        primary_key=True,
    )


class MagicItem(db.Model):
    """MagicItem."""

    __tablename__ = "magic_items"

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
        secondary="items_variants",
        primaryjoin=(ItemVariant.original_item_id == id),
        secondaryjoin=(ItemVariant.variant_item_id == id),
    )

    is_variant = db.Column(
        db.Boolean,
        default=False,
    )

    description = db.Column(
        db.ARRAY(db.Text),
        nullable=False,
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=True,
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

    last_updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    def __repr__(self):
        return f"<Magic Item #{self.id}: {self.name}, {self.item_type}>"


class ItemCollection(db.Model):
    """Mapping Items to Collections"""

    __tablename__ = "items_collections"

    item_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "magic_items.id",
            ondelete="cascade",
        ),
        primary_key=True,
    )

    collection_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "collections.id",
            ondelete="cascade",
        ),
        primary_key=True,
    )

    inventory = db.Column(
        db.Integer,
        default=1,
    )


class Collection(db.Model):
    """A Collection of Items Made by a User."""

    __tablename__ = "collections"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(db.Text)

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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="cascade",
        ),
        nullable=True,
    )

    items = db.relationship(
        "MagicItem", secondary="items_collections", backref="collection"
    )
