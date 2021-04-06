from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Email

from ..utils.mixins import please_enter

class OrderForm(FlaskForm):
    '''
    OrderForm:
    This Class defines the structure an validation to make an order of a the unique product
    '''
    customer_name = StringField('Name', validators=[DataRequired()])
    customer_address = StringField('Address', validators=[DataRequired()])
    customer_mobile = StringField('Mobile', validators=[DataRequired()])
    customer_email = TextField(
        'Email',
        validators=[
            please_enter('your', 'email address'),
            Email('Please enter a valid email address')
        ]
    )
