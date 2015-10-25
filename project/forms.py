from flask.ext.wtf import Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import InputRequired, ValidationError, EqualTo


class RegistrationForm(Form):
    """
    Register a new user.
    """
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
        InputRequired(), 
        EqualTo('password_again', message='Passwords must match')
    ])
    password_again = PasswordField('Password (again)')

    def validate_password_again(self, field):
        """
        Ensure both password fields match, otherwise raise a ValidationError.
        :raises: ValidationError if passwords don't match.
        """
        if self.password.data != field.data:
            raise ValidationError("Passwords don't match.")


class AddContactForm(Form):
    """
    Add a contact
    """
    name = StringField('Name:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired()])


class AddUserForm(Form):
    """
    Add a user to an account
    """
    email = StringField('Email', validators=[InputRequired()])
