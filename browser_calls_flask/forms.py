from flask_wtf import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError

from .validators import is_valid_number


class SupportTicketForm(Form):
        name = StringField('Name', validators=[DataRequired()])
        phone_number = StringField('Phone Number', description='Must include international prefix - e.g. +1 555 555 55555', validators=[DataRequired()])
        description = TextAreaField('Description', description='A description of your problem', validators=[DataRequired()])

        def validate_phone_number(form, field):
            if not is_valid_number(field.data):
                raise ValidationError("Invalid phone number!")
