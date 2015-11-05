from flask.ext.wtf import Form
from wtforms.fields import StringField, TextField
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
    content = TextField('Content:', validators=[InputRequired()])
