from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class ListAddForm(FlaskForm):
    """Form for adding users."""

    name = StringField('List Name', validators=[DataRequired()])
    description = StringField('Description (Optional)')
