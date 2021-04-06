from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

from ..utils.mixins import please_enter

class LoginForm(FlaskForm):
    '''
    LoginForm:
    This Class defines the structure an validation of the Login form
    '''
    username = TextField('Username', validators=[please_enter('your', 'username'),])
    password = PasswordField('Password', validators=[please_enter('your', 'password')])
    remember_me = BooleanField('Remember me.')

class RegisterForm(FlaskForm):
    '''
    RegisterForm:
    This Class defines the structure an validation of the SingUp form
    '''
    name = StringField('Name', validators=[please_enter('your', 'name')])
    # email = TextField(
    #     'Email',
    #     validators=[
    #         please_enter('your', 'email address'),
    #         Email('Please enter a valid email address')
    #     ]
    # )
    username = TextField('Username', validators=[please_enter('username'),])
    password = PasswordField(
        'Password',
        validators=[
            please_enter('password'),
            EqualTo('confirm_password', message='Passwords must match')
        ]
    )
    confirm_password = PasswordField()
    # recaptcha = RecaptchaField()
