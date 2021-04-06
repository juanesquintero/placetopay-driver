from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Email

from ..utils.mixins import please_enter

class OrderForm(FlaskForm):
    '''
    OrderForm:
    This Class defines the structure an validation to make an order of a the unique product
    '''
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Cell Phone', validators=[DataRequired()])
    email = TextField(
        'Email',
        validators=[
            please_enter('your', 'email address'),
            Email('Please enter a valid email address')
        ]
    )
