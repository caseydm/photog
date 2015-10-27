from flask.ext.wtf import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class AddContactForm(Form):
    """
    Add a contact
    """
    name = StringField('Name:', validators=[InputRequired()])
    email = StringField('Email:', validators=[InputRequired()])
