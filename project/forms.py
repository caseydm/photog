from flask.ext.wtf import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, DataRequired


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


class AddContactForm(Form):
    """
    Add a contact
    """
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])


class AddUserForm(Form):
    """
    Add a user to an account
    """
    email = StringField('Email', validators=[DataRequired()])
