from flask.ext.wtf import Form
from wtforms.fields import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, Email


class AddContactForm(Form):
    """
    Add a contact
    """
    name = StringField('Name:')
    email = StringField('Email:')
    phone = StringField('Phone:')
    lead_source = SelectField('Lead Source', choices=[
            ('', ''),
            ('Web Site', 'Web Site'),
            ('Phone', 'Phone'),
            ('Event', 'Event')
        ])
    comment = TextAreaField('Comment')


class AddNoteForm(Form):
    """
    Add a note to a contact
    """
    content = TextAreaField('Content:')
