from flask.ext.wtf import Form
from wtforms.fields import StringField
from wtforms.validators import InputRequired


class AddContactForm(Form):
    """
    Add a contact
    """
    name = StringField('Name:', validators=[InputRequired()])
    email = StringField('Email:')
    phone = StringField('Phone:')


class AddNoteForm(Form):
    """
    Add a note to a contact
    """
    content = StringField('Content:', validators=[InputRequired()])
