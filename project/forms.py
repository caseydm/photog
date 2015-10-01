from flask.ext.wtf import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired


class RegistrationForm(Form):
    """
    Register a new user.
    """
    username = StringField('Username')
    given_name = StringField('First Name')
    middle_name = StringField('Middle Name')
    surname = StringField('Last Name')
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
