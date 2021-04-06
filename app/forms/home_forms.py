from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class HomeForm(FlaskForm):
    '''
    HomeForm:
    This Class defines the structure an validation of the home form
    '''
    name = StringField('Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
