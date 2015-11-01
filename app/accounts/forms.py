from flask.ext.wtf import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo


class RegistrationForm(Form):
    """
    Register a new user.
    """
    email = StringField('Email', validators=[
        InputRequired('Email field is required')
        ])
    password = PasswordField('Password', validators=[
        InputRequired('Password field is required'),
        EqualTo('password_again', message='Passwords must match')
        ])
    password_again = PasswordField('Password (again)')


class AddUserForm(Form):
    """
    Add a user to an account
    """
    email = StringField('Email', validators=[
        InputRequired('Email field is required')
        ])
