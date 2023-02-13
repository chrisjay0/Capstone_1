from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from magic_items.services import ITEM_RARITY, ITEM_TYPES


class ItemForm(FlaskForm):
    """Form for adding and editing items."""

    name = StringField("Magic Item Name", validators=[DataRequired()])
    item_type = SelectField("Magic Item Type", choices=ITEM_TYPES)
    rarity = SelectField("Rarity", choices=ITEM_RARITY)
    description = TextAreaField("Description", validators=[DataRequired()])


class CollectionAddForm(FlaskForm):
    """Form for adding and editing collections."""

    name = StringField("List Name", validators=[DataRequired()])
    description = StringField("Description (Optional)")


class ItemFilterForm(FlaskForm):
    """Form for filtering items."""

    class Meta:
        csrf = False

    item_type = SelectField("Magic Item Type", choices=[""] + ITEM_TYPES)
    rarity = SelectField("Rarity", choices=[""] + ITEM_RARITY)
    source = SelectField("Source", choices=["", "dnd5eapi", "user"])
