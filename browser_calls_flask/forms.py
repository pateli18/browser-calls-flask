from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class SupportTicketForm(Form):
        name = StringField('name', validators=[DataRequired()])
        phone_number = StringField('phone_number', validators=[DataRequired()])
        description = StringField('description', validators=[DataRequired()])
