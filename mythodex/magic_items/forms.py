from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

from magic_items.services import ITEM_RARITY, ITEM_TYPES

class ItemAddForm(FlaskForm):
    """Form for adding users."""

    name = StringField('Magic Item Name', validators=[DataRequired()])
    item_type = SelectField("Magic Item Type",choices=ITEM_TYPES)
    rarity = SelectField("Rarity",choices=ITEM_RARITY)
    has_variants = StringField('List Name', validators=[DataRequired()])
    is_variant = StringField('List Name', validators=[DataRequired()])
    description = StringField('List Name', validators=[DataRequired()])

class CollectionAddForm(FlaskForm):
    """Form for adding users."""

    name = StringField('List Name', validators=[DataRequired()])
    description = StringField('Description (Optional)')